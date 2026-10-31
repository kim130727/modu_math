from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Assignment,
    AssignmentItem,
    AssignmentProgress,
    AssignmentRecipient,
    Classroom,
    Enrollment,
    Mastery,
    ProblemSet,
    ProblemSetItem,
    StudentProfile,
)
from .platform_permissions import IsTeacherOrAdmin, is_manager, owned
from .platform_serializers import (
    AnswerSubmissionSerializer,
    AssignmentCreateSerializer,
    AssignmentStatusSerializer,
    ClassroomSerializer,
    DraftSerializer,
    HintRequestSerializer,
    EnrollmentRequestSerializer,
    EnrollmentSerializer,
    JoinSerializer,
    ProblemSetSerializer,
    ReviewSerializer,
    StudentCreateSerializer,
    UserAccessSerializer,
)
from .services.assignments import (
    latest_attempts,
    recipient_result,
    record_answer,
    released,
    require_open,
    reveal_hint,
    snapshot_item,
    submit_assignment,
)


def validated(serializer_type, data, **kwargs):
    serializer = serializer_type(data=data, **kwargs)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def allowed_students(user):
    qs = StudentProfile.objects.select_related("user")
    if user.is_staff or user.is_superuser:
        return qs
    return qs.filter(
        Q(created_by=user)
        | Q(enrollments__classroom__teacher=user, enrollments__status="approved")
    ).distinct()


def student_data(student):
    return {
        "id": student.pk,
        "user_id": student.user_id,
        "username": student.user.username,
    }


class StudentViewSet(viewsets.GenericViewSet):
    permission_classes = (IsTeacherOrAdmin,)

    def get_queryset(self):
        return allowed_students(self.request.user)

    def list(self, request):
        return Response([student_data(s) for s in self.get_queryset().order_by("pk")])

    def retrieve(self, request, pk=None):
        return Response(student_data(self.get_object()))

    @transaction.atomic
    def create(self, request):
        data = validated(StudentCreateSerializer, request.data)
        user = get_user_model().objects.create_user(**data)
        profile = StudentProfile.objects.create(user=user, created_by=request.user)
        return Response(student_data(profile), status=201)


class ClassroomViewSet(viewsets.ModelViewSet):
    permission_classes = (IsTeacherOrAdmin,)
    serializer_class = ClassroomSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        return owned(Classroom.objects.all(), self.request.user, "teacher").order_by(
            "pk"
        )

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    @action(detail=True, methods=["get", "post"])
    def enrollments(self, request, pk=None):
        classroom = self.get_object()
        if request.method == "GET":
            return Response(
                EnrollmentSerializer(
                    classroom.enrollments.select_related("student__user"), many=True
                ).data
            )
        data = validated(EnrollmentRequestSerializer, request.data)
        student = get_object_or_404(
            allowed_students(request.user), pk=data["student_id"]
        )
        if classroom.archived:
            raise ValidationError("보관한 학급입니다.")
        enrollment, _ = Enrollment.objects.update_or_create(
            classroom=classroom, student=student, defaults={"status": "approved"}
        )
        return Response(EnrollmentSerializer(enrollment).data, status=201)

    @action(
        detail=True,
        methods=["patch"],
        url_path=r"enrollments/(?P<enrollment_id>[^/.]+)",
    )
    def enrollment(self, request, pk=None, enrollment_id=None):
        classroom = self.get_object()
        enrollment = get_object_or_404(classroom.enrollments, pk=enrollment_id)
        serializer = EnrollmentSerializer(enrollment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="rotate-code")
    def rotate_code(self, request, pk=None):
        from .platform_models import invite_code

        classroom = self.get_object()
        classroom.invite_code = invite_code()
        classroom.save(update_fields=("invite_code",))
        return Response(self.get_serializer(classroom).data)


class JoinClassView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        if is_manager(request.user):
            raise ValidationError("학생 계정으로만 학급에 가입할 수 있습니다.")
        data = validated(JoinSerializer, request.data)
        classroom = get_object_or_404(
            Classroom, invite_code=data["invite_code"], archived=False
        )
        student, _ = StudentProfile.objects.get_or_create(user=request.user)
        enrollment, _ = Enrollment.objects.get_or_create(
            classroom=classroom, student=student
        )
        if enrollment.status == "inactive":
            enrollment.status = "pending"
            enrollment.save(update_fields=("status",))
        return Response(
            {
                "id": enrollment.pk,
                "classroom": classroom.name,
                "status": enrollment.status,
            },
            status=201,
        )


class StudentClassesView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        enrollments = Enrollment.objects.filter(
            student__user=request.user, classroom__archived=False
        ).select_related("classroom__teacher")
        return Response(
            [
                {
                    "id": e.classroom_id,
                    "name": e.classroom.name,
                    "teacher_name": e.classroom.teacher.username,
                    "status": e.status,
                }
                for e in enrollments.order_by("classroom_id")
            ]
        )


class ProblemSetViewSet(viewsets.ModelViewSet):
    permission_classes = (IsTeacherOrAdmin,)
    serializer_class = ProblemSetSerializer
    http_method_names = ["get", "post", "put", "patch", "head", "options"]

    def get_queryset(self):
        return owned(
            ProblemSet.objects.prefetch_related("items"), self.request.user
        ).order_by("pk")

    @transaction.atomic
    def perform_create(self, serializer):
        problems = serializer.validated_data.pop("problem_ids")
        problem_set = serializer.save(owner=self.request.user)
        ProblemSetItem.objects.bulk_create(
            [
                ProblemSetItem(problem_set=problem_set, problem=p, position=i)
                for i, p in enumerate(problems)
            ]
        )

    @transaction.atomic
    def perform_update(self, serializer):
        current = ProblemSet.objects.select_for_update().get(pk=serializer.instance.pk)
        problems = serializer.validated_data.pop("problem_ids", None)
        serializer.instance = current
        problem_set = serializer.save(version=current.version + 1)
        if problems is not None:
            problem_set.items.all().delete()
            ProblemSetItem.objects.bulk_create(
                [
                    ProblemSetItem(problem_set=problem_set, problem=p, position=i)
                    for i, p in enumerate(problems)
                ]
            )

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def duplicate(self, request, pk=None):
        original = self.get_object()
        from .services.problem_access import require_reusable

        require_reusable(
            request.user,
            [item.problem for item in original.items.select_related("problem")],
        )
        duplicate = ProblemSet.objects.create(
            owner=request.user,
            title=original.title + " (복제)",
            description=original.description,
        )
        ProblemSetItem.objects.bulk_create(
            [
                ProblemSetItem(
                    problem_set=duplicate,
                    problem_id=item.problem_id,
                    position=item.position,
                )
                for item in original.items.all()
            ]
        )
        return Response(self.get_serializer(duplicate).data, status=201)


class AssignmentViewSet(viewsets.GenericViewSet):
    permission_classes = (IsTeacherOrAdmin,)

    def get_queryset(self):
        return owned(
            Assignment.objects.select_related("problem_set"), self.request.user
        ).order_by("-pk")

    def summary(self, assignment):
        recipients = list(assignment.recipients.select_related("student__user"))
        results = [recipient_result(r, teacher=True) for r in recipients]
        total = assignment.items.count()
        return {
            "id": assignment.pk,
            "title": assignment.title,
            "problem_set": assignment.problem_set_id,
            "source_version": assignment.source_version,
            "status": assignment.status,
            "starts_at": assignment.starts_at,
            "due_at": assignment.due_at,
            "release_policy": assignment.release_policy,
            "max_attempts": assignment.max_attempts,
            "item_count": total,
            "recipient_count": len(recipients),
            "submitted_count": sum(r.submitted_at is not None for r in recipients),
            "accuracy": (
                sum(r["correct"] for r in results) / (total * len(recipients))
                if total and recipients
                else 0
            ),
        }

    def list(self, request):
        return Response([self.summary(a) for a in self.get_queryset()])

    def retrieve(self, request, pk=None):
        assignment = self.get_object()
        return Response(self.summary(assignment))

    @transaction.atomic
    def create(self, request):
        data = validated(AssignmentCreateSerializer, request.data)
        problem_set = get_object_or_404(
            owned(ProblemSet.objects.select_for_update(), request.user),
            pk=data.pop("problem_set").pk,
        )
        student_ids = set(data.pop("student_ids", []))
        class_ids = set(data.pop("class_ids", []))
        classes = owned(
            Classroom.objects.filter(archived=False), request.user, "teacher"
        ).filter(pk__in=class_ids)
        if classes.count() != len(class_ids):
            raise ValidationError({"class_ids": "허용되지 않은 학급입니다."})
        if allowed_students(request.user).filter(pk__in=student_ids).count() != len(
            student_ids
        ):
            raise ValidationError({"student_ids": "허용되지 않은 학생입니다."})
        student_ids.update(
            Enrollment.objects.filter(
                classroom__in=classes, status="approved"
            ).values_list("student_id", flat=True)
        )
        if not student_ids:
            raise ValidationError("배정할 학생이 없습니다.")
        items = list(problem_set.items.select_related("problem"))
        if not items:
            raise ValidationError("빈 문제집은 배정할 수 없습니다.")
        from .services.problem_access import require_reusable

        require_reusable(request.user, [item.problem for item in items])
        assignment = Assignment.objects.create(
            owner=request.user,
            problem_set=problem_set,
            source_version=problem_set.version,
            **data,
        )
        for item in items:
            snapshot_item(assignment, item.problem, item.position)
        AssignmentRecipient.objects.bulk_create(
            [
                AssignmentRecipient(assignment=assignment, student_id=pk)
                for pk in sorted(student_ids)
            ]
        )
        return Response(self.summary(assignment), status=201)

    def partial_update(self, request, pk=None):
        assignment = self.get_object()
        data = validated(AssignmentStatusSerializer, request.data)
        assignment.status = data["status"]
        assignment.save(update_fields=("status",))
        return Response(self.summary(assignment))

    @action(detail=True, methods=["get"])
    def recipients(self, request, pk=None):
        assignment = self.get_object()
        return Response(
            [
                recipient_result(r, teacher=True, detail=True)
                for r in assignment.recipients.select_related("student__user")
            ]
        )

    @action(detail=True, methods=["get"])
    def results(self, request, pk=None):
        assignment = self.get_object()
        recipients = list(assignment.recipients.select_related("student__user"))
        rows = [recipient_result(r, teacher=True) for r in recipients]
        last = [latest_attempts(r) for r in recipients]
        items = []
        for item in assignment.items.all():
            attempts = [m[item.pk] for m in last if item.pk in m]
            items.append(
                {
                    "item_id": item.pk,
                    "position": item.position,
                    "answered": len(attempts),
                    "correct": sum(a.is_correct for a in attempts),
                    "accuracy": (
                        sum(a.is_correct for a in attempts) / len(recipients)
                        if recipients
                        else 0
                    ),
                    "elapsed_ms": sum(a.elapsed_ms for a in attempts),
                    "concepts": item.concepts,
                }
            )
        concepts = {}
        for item in items:
            for concept in item["concepts"]:
                metric = concepts.setdefault(concept, {"correct": 0, "total": 0})
                metric["correct"] += item["correct"]
                metric["total"] += len(recipients)
        return Response(
            {
                "assignment": self.summary(assignment),
                "recipients": rows,
                "items": items,
                "concepts": concepts,
                "unsubmitted_recipient_ids": [
                    r.pk for r in recipients if r.submitted_at is None
                ],
            }
        )

    @action(detail=True, methods=["post"], url_path="reassign-wrong")
    @transaction.atomic
    def reassign_wrong(self, request, pk=None):
        assignment = self.get_object()
        data = validated(ReviewSerializer, request.data)
        recipient = get_object_or_404(assignment.recipients, pk=data["recipient_id"])
        if not recipient.submitted_at:
            raise ValidationError("제출 완료한 과제만 복습으로 배정할 수 있습니다.")
        wrong = [
            key
            for key, attempt in latest_attempts(recipient).items()
            if not attempt.is_correct
        ]
        if not wrong:
            raise ValidationError("오답 문항이 없습니다.")
        review = Assignment.objects.create(
            owner=request.user,
            problem_set=assignment.problem_set,
            source_version=assignment.source_version,
            title=data["title"],
            release_policy="after_submission",
            max_attempts=assignment.max_attempts,
        )
        for i, source in enumerate(assignment.items.filter(pk__in=wrong)):
            AssignmentItem.objects.create(
                assignment=review,
                problem=source.problem,
                position=i,
                public_content=source.public_content,
                answer=source.answer,
                solution=source.solution,
                concepts=source.concepts,
                hints=source.hints,
            )
        AssignmentRecipient.objects.create(assignment=review, student=recipient.student)
        return Response(self.summary(review), status=201)


class StudentAssignmentViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # The URL id is Assignment.id, not the recipient id.
        return AssignmentRecipient.objects.filter(
            student__user=self.request.user
        ).select_related("assignment")

    def get_object(self):
        return get_object_or_404(self.get_queryset(), assignment_id=self.kwargs["pk"])

    def list(self, request):
        return Response(
            [
                recipient_result(r)
                for r in self.get_queryset().order_by("-assignment_id")
            ]
        )

    def retrieve(self, request, pk=None):
        recipient = self.get_object()
        if (
            recipient.assignment.starts_at
            and timezone.now() < recipient.assignment.starts_at
        ):
            return Response(recipient_result(recipient))
        return Response(recipient_result(recipient, detail=True))

    @action(detail=True, methods=["post"])
    def hints(self, request, pk=None):
        recipient = self.get_object()
        data = validated(HintRequestSerializer, request.data)
        return Response(
            reveal_hint(recipient.pk, request.user, data["item_id"], data["level"])
        )

    @action(detail=True, methods=["post"])
    def answers(self, request, pk=None):
        recipient = self.get_object()
        data = validated(AnswerSubmissionSerializer, request.data)
        recipient, attempt, created = record_answer(recipient.pk, request.user, data)
        result = {
            "attempt_id": attempt.pk,
            "item_id": attempt.assignment_item_id,
            "attempt_number": attempt.assignment_try,
        }
        if released(recipient):
            result["is_correct"] = attempt.is_correct
        return Response(result, status=201 if created else 200)

    @action(detail=True, methods=["put"])
    @transaction.atomic
    def progress(self, request, pk=None):
        obj = self.get_object()
        recipient = AssignmentRecipient.objects.select_for_update().get(pk=obj.pk)
        require_open(recipient)
        data = validated(DraftSerializer, request.data)
        item = get_object_or_404(recipient.assignment.items, pk=data["item_id"])
        AssignmentProgress.objects.update_or_create(
            recipient=recipient, item=item, defaults={"answer": data["answer"]}
        )
        return Response({"saved": True})

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        recipient = self.get_object()
        recipient = submit_assignment(recipient.pk, request.user)
        return Response(recipient_result(recipient, detail=True))


class TeacherDashboardView(APIView):
    permission_classes = (IsTeacherOrAdmin,)

    def get(self, request):
        assignments = owned(Assignment.objects.all(), request.user)
        recipients = AssignmentRecipient.objects.filter(assignment__in=assignments)
        return Response(
            {
                "students": allowed_students(request.user).count(),
                "classes": owned(
                    Classroom.objects.filter(archived=False), request.user, "teacher"
                ).count(),
                "assignments": assignments.count(),
                "recipients": recipients.count(),
                "submitted": recipients.filter(submitted_at__isnull=False).count(),
                "unsubmitted": recipients.filter(submitted_at__isnull=True).count(),
                "statistics_scope": "owned_assignments",
            }
        )


class AdminUserViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = get_user_model().objects.all().order_by("pk")

    def representation(self, user):
        from .serializers import RegisterSerializer

        return {
            "id": user.pk,
            "username": user.username,
            "is_active": user.is_active,
            "role": RegisterSerializer(user).data["role"],
        }

    def list(self, request):
        page = self.paginate_queryset(self.get_queryset())
        return self.get_paginated_response([self.representation(user) for user in page])

    def retrieve(self, request, pk=None):
        return Response(self.representation(self.get_object()))

    @transaction.atomic
    def partial_update(self, request, pk=None):
        from django.contrib.auth.models import Group
        from rest_framework.exceptions import PermissionDenied

        user = get_object_or_404(self.get_queryset().select_for_update(), pk=pk)
        data = validated(UserAccessSerializer, request.data)
        if user.is_superuser or user.is_staff or data.get("role") == "admin":
            if not request.user.is_superuser:
                raise PermissionDenied("관리자 권한 변경은 최고 관리자만 가능합니다.")
        if user.is_superuser:
            raise ValidationError("최고 관리자 계정은 서버 관리 절차로 변경해 주세요.")
        if user == request.user and (
            data.get("is_active") is False or data.get("role") in {"student", "teacher"}
        ):
            raise ValidationError("자신의 관리 권한을 제거할 수 없습니다.")
        if "role" in data:
            group, _ = Group.objects.get_or_create(name="modu_teachers")
            if data["role"] == "teacher":
                user.groups.add(group)
            else:
                user.groups.remove(group)
            user.is_staff = data["role"] == "admin"
            if data["role"] == "student":
                StudentProfile.objects.get_or_create(user=user)
        if "is_active" in data:
            user.is_active = data["is_active"]
        user.save(update_fields=("is_staff", "is_active"))
        return Response(self.representation(user))


class CurrentUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        from .serializers import RegisterSerializer

        return Response(RegisterSerializer(request.user).data)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if request.auth:
            request.auth.delete()
        response = Response(status=204)
        response.delete_cookie("modu_editor_session", path="/", samesite="Strict")
        return response


class EditorSessionView(APIView):
    """Short-lived image credentials; API writes still require a token header."""

    permission_classes = (IsTeacherOrAdmin,)

    def post(self, request):
        from django.conf import settings

        response = Response(status=204)
        response.set_signed_cookie(
            "modu_editor_session",
            request.auth.key,
            salt="modu.editor.session.v1",
            path="/",
            max_age=3600,
            secure=not settings.DEBUG,
            httponly=True,
            samesite="Strict",
        )
        return response
