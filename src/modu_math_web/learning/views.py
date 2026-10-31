from __future__ import annotations

from django.conf import settings
from django.http import FileResponse
from django.utils import timezone
from django.db.models import Q
from django.db import connection
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Attempt, Mastery, Problem, ProblemTagging
from .serializers import (
    AttemptSerializer,
    LoginSerializer,
    MasterySerializer,
    ProblemDetailSerializer,
    ProblemListSerializer,
    ProblemTaggingSerializer,
    RegisterSerializer,
)
from .services.diagnostics_service import DiagnosticService
from .services.recommendation_service import ProblemRecommendationService
from .platform_permissions import is_manager
from .services.assignments import student_problem, visible_attempts


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user": RegisterSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.pk,
                    "username": user.get_username(),
                    "email": user.email,
                    "is_staff": user.is_staff,
                    "role": RegisterSerializer(user).data["role"],
                },
            }
        )


class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Problem.objects.select_related("publication").all()

    def get_serializer_class(self):
        return (
            ProblemListSerializer if self.action == "list" else ProblemDetailSerializer
        )

    def get_queryset(self):
        from .services.problem_access import accessible_problems, public_condition

        queryset = accessible_problems(self.request.user)
        scope = self.request.query_params.get("scope", "")
        if scope == "public":
            queryset = queryset.filter(public_condition())
        elif scope == "mine":
            queryset = (
                queryset.filter(publication__owner=self.request.user)
                if self.request.user.is_authenticated
                else queryset.none()
            )
        elif scope == "class":
            queryset = queryset.filter(publication__visibility="class")
        classroom_id = self.request.query_params.get("classroom")
        if classroom_id:
            try:
                classroom_id = int(classroom_id)
            except ValueError as exc:
                raise ValidationError(
                    {"classroom": "클래스 번호가 올바르지 않습니다."}
                ) from exc
            queryset = queryset.filter(
                publication__visibility="class",
                publication__classrooms__pk=classroom_id,
            ).distinct()
        ids = self.request.query_params.get("ids")
        if ids:
            try:
                values = [int(value) for value in ids.split(",")]
                if len(values) > 200 or any(value < 1 for value in values):
                    raise ValueError()
            except ValueError as exc:
                raise ValidationError(
                    {"ids": "최대 200개의 양수 ID를 입력해 주세요."}
                ) from exc
            queryset = queryset.filter(pk__in=values)
        visibility = self.request.query_params.get("visibility")
        if visibility:
            queryset = queryset.filter(publication__visibility=visibility)
        for parameter in ("language", "problem_type"):
            value = self.request.query_params.get(parameter)
            if value not in (None, ""):
                queryset = queryset.filter(**{parameter: value})
        grade = self.request.query_params.get("grade")
        if grade not in (None, ""):
            try:
                queryset = queryset.filter(grade=int(grade))
            except ValueError as exc:
                raise ValidationError({"grade": "grade는 정수여야 합니다."}) from exc
        unit = self.request.query_params.get("unit")
        if unit:
            queryset = queryset.filter(
                Q(catalog_data__unit__icontains=unit)
                | Q(catalog_data__unitTopic__icontains=unit)
                | Q(catalog_data__topic__icontains=unit)
            )
        concept = self.request.query_params.get("concept")
        if concept:
            if connection.features.supports_json_field_contains:
                queryset = queryset.filter(concepts__contains=[concept])
            else:
                # SQLite JSON storage escapes Korean text; LIKE on the JSON
                # document does not implement tag membership consistently.
                matches = [
                    pk
                    for pk, tags in queryset.values_list("pk", "concepts")
                    if concept in tags
                ]
                queryset = queryset.filter(pk__in=matches)
        for parameter, field in (
            ("difficulty", "publication__difficulty"),
            ("status", "publication__status"),
        ):
            value = self.request.query_params.get(parameter)
            if value:
                if parameter == "difficulty":
                    try:
                        value = int(value)
                    except ValueError as exc:
                        raise ValidationError(
                            {parameter: "정수가 필요합니다."}
                        ) from exc
                if (parameter == "status" and value == "published") or (
                    parameter == "difficulty" and value == 1
                ):
                    queryset = queryset.filter(
                        Q(publication__isnull=True) | Q(**{field: value})
                    )
                else:
                    queryset = queryset.filter(**{field: value})
        return queryset

    def retrieve(self, request, *args, **kwargs):
        from .services.problem_access import can_edit, reusable_problems

        problem = self.get_object()
        context = {"request": request}
        if (
            can_edit(request.user, problem)
            or reusable_problems(request.user).filter(pk=problem.pk).exists()
        ):
            from .services.assignment_content import freeze_images

            data = ProblemDetailSerializer(problem, context=context).data
            from copy import deepcopy

            data["renderer_data"] = freeze_images(
                {"renderer_data": deepcopy(problem.renderer_data)}, problem
            )["renderer_data"]
            return Response(data)
        from .services.assignment_content import freeze_images

        return Response(
            {
                **ProblemListSerializer(problem, context=context).data,
                **freeze_images(student_problem(problem), problem),
            }
        )

    @action(detail=True, methods=["get", "patch"])
    def publication(self, request, pk=None):
        from rest_framework.exceptions import PermissionDenied
        from .models import ProblemPublication
        from .platform_serializers import PublicationSerializer

        if not is_manager(request.user):
            raise PermissionDenied()
        problem = self.get_object()
        from .services.problem_access import can_edit

        if not can_edit(request.user, problem):
            raise PermissionDenied("문제 작성자만 공개 범위를 변경할 수 있습니다.")
        if request.method == "GET":
            publication = ProblemPublication.objects.filter(problem=problem).first()
            return Response(
                PublicationSerializer(publication, context={"request": request}).data
                if publication
                else {
                    "status": "published",
                    "difficulty": 1,
                    "visibility": "public",
                    "classroom_ids": [],
                    "allow_classroom_use": True,
                    "rights_confirmed": True,
                    "source_credit": "",
                    "rights_note": "",
                }
            )
        publication = ProblemPublication.objects.filter(problem=problem).first()
        serializer = PublicationSerializer(
            publication, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        publication = serializer.save(
            problem=problem,
            updated_by=request.user,
            **(
                {"status": serializer.validated_data.get("status", "published")}
                if publication is None
                else {}
            ),
        )
        return Response(PublicationSerializer(publication).data)

    @action(detail=True, methods=["get"], url_path="asset")
    def asset(self, request, pk=None):
        problem = self.get_object()
        filename = request.query_params.get("filename", "")
        if not filename or filename != filename.replace("\\", "/").split("/")[-1]:
            raise ValidationError({"filename": "올바른 파일 이름이 필요합니다."})
        if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".svg")):
            raise ValidationError(
                {"filename": "문제 이미지 파일만 요청할 수 있습니다."}
            )
        # A neighboring problem's preview must not be fetched using a public id.
        from urllib.parse import unquote, urlsplit

        referenced = {
            unquote(urlsplit(str(e.get("attributes", {}).get("href", ""))).path)
            .replace("\\", "/")
            .split("/")[-1]
            for e in problem.renderer_data.get("elements", [])
            if e.get("type") == "image"
        }
        prefix_name = str(problem.catalog_data.get("filePrefix") or problem.problem_id)
        if filename not in referenced:
            from rest_framework.exceptions import NotFound

            # Only authors can read the full SVG; it may contain answer overlays.
            from .services.problem_access import can_edit

            if filename != prefix_name + ".svg" or not can_edit(request.user, problem):
                raise NotFound()
        root = settings.PROBLEMS_ROOT.resolve()
        catalog_path = str(problem.catalog_data.get("path") or "")
        prefix = "examples/problems/"
        relative_directory = (
            catalog_path[len(prefix) :]
            if catalog_path.startswith(prefix)
            else problem.language
        )
        problem_directory = (root / relative_directory).resolve()
        try:
            problem_directory.relative_to(root)
        except ValueError:
            problem_directory = root / problem.language
        asset_path = (problem_directory / filename).resolve()
        if not asset_path.is_relative_to(root):
            raise ValidationError({"filename": "허용되지 않은 경로입니다."})
        if not asset_path.is_file():
            from rest_framework.exceptions import NotFound

            raise NotFound("문제 자산을 찾을 수 없습니다.")
        return FileResponse(asset_path.open("rb"), filename=filename)


class AttemptViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AttemptSerializer

    def get_queryset(self):
        queryset = visible_attempts(
            Attempt.objects.filter(user=self.request.user)
        ).select_related("problem")
        problem_id = self.request.query_params.get("problem_id")
        if problem_id:
            queryset = queryset.filter(problem__problem_id=problem_id)
        return queryset


class MasteryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MasterySerializer

    def get_queryset(self):
        queryset = Mastery.objects.filter(user=self.request.user)
        tag_type = self.request.query_params.get("tag_type")
        if tag_type:
            queryset = queryset.filter(tag_type=tag_type)
        # Stored Mastery is an internal all-time aggregate. Public responses
        # must not expose unreleased assignment grades through score changes.
        attempts = Attempt.objects.filter(user=self.request.user)
        visible = visible_attempts(attempts)
        if visible.count() == attempts.count():
            return queryset
        metrics = {}
        for attempt in visible.select_related("problem", "assignment_item").order_by(
            "created_at"
        ):
            concepts = (
                attempt.assignment_item.concepts
                if attempt.assignment_item_id
                else set(attempt.problem.effective_concepts + attempt.problem.concepts)
            )
            for concept in concepts:
                metric = metrics.setdefault(concept, [0, 0, None])
                metric[0] += 1
                metric[1] += int(attempt.is_correct)
                metric[2] = attempt.created_at
        result = []
        for mastery in queryset:
            if mastery.concept in metrics:
                count, correct, last = metrics[mastery.concept]
                mastery.attempt_count, mastery.correct_count = count, correct
                mastery.score, mastery.last_practiced_at = correct / count, last
                result.append(mastery)
        return result


class ProblemTaggingViewSet(viewsets.ModelViewSet):
    """Admin-only viewset for reviewing, modifying, and confirming problem tags."""

    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ProblemTaggingSerializer
    queryset = ProblemTagging.objects.select_related("problem", "reviewed_by").all()

    def get_queryset(self):
        queryset = super().get_queryset()
        problem_id = self.request.query_params.get("problem_id")
        if problem_id:
            queryset = queryset.filter(problem__problem_id=problem_id)
        status_val = self.request.query_params.get("review_status")
        if status_val:
            queryset = queryset.filter(review_status=status_val)
        low_confidence = self.request.query_params.get("low_confidence")
        if low_confidence:
            try:
                queryset = queryset.filter(confidence__lt=float(low_confidence))
            except ValueError:
                pass
        return queryset

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        tagging = self.get_object()
        reviewed_concepts = request.data.get("reviewed_concepts")
        reviewed_skills = request.data.get("reviewed_skills")

        if reviewed_concepts is not None:
            tagging.reviewed_concepts = reviewed_concepts
        elif tagging.reviewed_concepts is None:
            tagging.reviewed_concepts = tagging.auto_concepts

        if reviewed_skills is not None:
            tagging.reviewed_skills = reviewed_skills
        elif tagging.reviewed_skills is None:
            tagging.reviewed_skills = tagging.auto_skills

        tagging.review_status = "confirmed"
        tagging.reviewed_by = request.user
        tagging.reviewed_at = timezone.now()
        tagging.save()

        # Sync back to Problem model
        problem = tagging.problem
        problem.concepts = tagging.effective_concepts
        problem.skills = tagging.effective_skills
        problem.save(update_fields=("concepts", "skills", "updated_at"))

        return Response(ProblemTaggingSerializer(tagging).data)


# --- Diagnostic Analytics Views ---


class DiagnosticSummaryView(APIView):
    """Returns overall student diagnostic summary metrics."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        service = DiagnosticService(request.user)
        return Response(service.get_summary())


class DiagnosticConceptsView(APIView):
    """Returns concept-level mastery and diagnostics for the current user."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        service = DiagnosticService(request.user)
        return Response(service.get_tag_diagnostics(tag_type="concept"))


class DiagnosticSkillsView(APIView):
    """Returns skill-level mastery and diagnostics for the current user."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        service = DiagnosticService(request.user)
        return Response(service.get_tag_diagnostics(tag_type="skill"))


class DiagnosticHistoryView(APIView):
    """Returns attempt solve history with tagged concepts and skills."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        service = DiagnosticService(request.user)
        limit = int(request.query_params.get("limit", 50))
        return Response(service.get_history(limit=limit))


class RecommendationsView(APIView):
    """Returns personalized problem recommendations across 5 priority tiers."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        service = ProblemRecommendationService(request.user)
        limit = int(request.query_params.get("limit", 10))
        language = request.query_params.get("language", "ko")
        return Response(service.get_recommendations(limit=limit, language=language))
