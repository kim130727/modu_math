from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import Attempt, Mastery, Problem


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    invite_code = serializers.CharField(write_only=True, required=False, max_length=64)
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        from .platform_permissions import is_manager

        return (
            "admin"
            if obj.is_staff or obj.is_superuser
            else "teacher" if is_manager(obj) else "student"
        )

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "invite_code", "role")
        read_only_fields = ("id",)

    def validate_invite_code(self, value):
        from .models import Classroom

        if not Classroom.objects.filter(invite_code=value, archived=False).exists():
            raise serializers.ValidationError("사용할 수 없는 학급 초대 코드입니다.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        from .models import Classroom, Enrollment, StudentProfile

        code = validated_data.pop("invite_code", None)
        user = get_user_model().objects.create_user(**validated_data)
        student = StudentProfile.objects.create(user=user)
        if code:
            classroom = Classroom.objects.filter(
                invite_code=code, archived=False
            ).first()
            if classroom is None:
                raise serializers.ValidationError(
                    {"invite_code": "사용할 수 없는 초대 코드입니다."}
                )
            Enrollment.objects.create(student=student, classroom=classroom)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs["username"],
            password=attrs["password"],
        )
        if user is None or not user.is_active:
            raise serializers.ValidationError(
                "아이디 또는 비밀번호가 올바르지 않습니다."
            )
        attrs["user"] = user
        return attrs


class ProblemListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()
    domain = serializers.SerializerMethodField()
    semester = serializers.SerializerMethodField()
    unit_number = serializers.SerializerMethodField()
    unit_topic = serializers.SerializerMethodField()
    sub_unit = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    file_prefix = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = (
            "id",
            "problem_id",
            "language",
            "grade",
            "problem_type",
            "concepts",
            "skills",
            "title",
            "subject",
            "unit",
            "domain",
            "semester",
            "unit_number",
            "unit_topic",
            "sub_unit",
            "topic",
            "file_prefix",
            "path",
            "updated_at",
        )

    def _catalog_value(self, obj, *keys, default=""):
        for key in keys:
            value = obj.catalog_data.get(key)
            if value not in (None, ""):
                return value
        return default

    def get_title(self, obj):
        metadata = obj.semantic_data.get("metadata", {})
        return self._catalog_value(
            obj,
            "title",
            default=metadata.get("title") or metadata.get("question") or obj.problem_id,
        )

    def get_subject(self, obj):
        return self._catalog_value(obj, "subject", default="math")

    def get_unit(self, obj):
        return self._catalog_value(obj, "unit", "unitTopic", "topic", default="미분류")

    def get_domain(self, obj):
        return self._catalog_value(obj, "domain", default="수학 개념")

    def get_semester(self, obj):
        return self._catalog_value(obj, "semester", default="1학기")

    def get_unit_number(self, obj):
        return self._catalog_value(obj, "unitNumber", default=1)

    def get_unit_topic(self, obj):
        return self._catalog_value(obj, "unitTopic", "unit", default="미분류")

    def get_sub_unit(self, obj):
        return self._catalog_value(obj, "subUnit", default="기본 학습")

    def get_topic(self, obj):
        return self._catalog_value(obj, "topic", "unitTopic", "unit", default="미분류")

    def get_file_prefix(self, obj):
        return self._catalog_value(obj, "filePrefix", default=obj.problem_id)

    def get_path(self, obj):
        return self._catalog_value(
            obj,
            "path",
            default=f"examples/problems/{obj.language}",
        )


class ProblemDetailSerializer(ProblemListSerializer):
    class Meta:
        model = Problem
        fields = ProblemListSerializer.Meta.fields + (
            "catalog_data",
            "answer",
            "semantic_data",
            "solvable_data",
            "layout_data",
            "renderer_data",
            "updated_at",
        )


class AttemptSerializer(serializers.ModelSerializer):
    problem = serializers.PrimaryKeyRelatedField(
        queryset=Problem.objects.all(), required=False
    )
    problem_id = serializers.CharField(required=False)
    problem_language = serializers.CharField(write_only=True, required=False)
    language = serializers.CharField(source="problem.language", read_only=True)

    class Meta:
        model = Attempt
        fields = (
            "id",
            "problem",
            "problem_id",
            "problem_language",
            "language",
            "submitted_answer",
            "is_correct",
            "elapsed_ms",
            "hint_count",
            "retry_count",
            "events",
            "session_id",
            "submitted_at",
            "created_at",
        )
        read_only_fields = ("id", "is_correct", "created_at")

    def validate_events(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("events는 배열이어야 합니다.")
        return value

    def validate(self, attrs):
        language = attrs.pop(
            "problem_language", self.initial_data.get("problem_language", "ko")
        )
        if "problem" not in attrs:
            raw_id = self.initial_data.get("problem_id")
            if not raw_id:
                raise serializers.ValidationError(
                    {"problem": "problem ID 또는 problem_id가 필요합니다."}
                )
            problem = Problem.objects.filter(
                problem_id=raw_id, language=language
            ).first()
            if not problem:
                raise serializers.ValidationError(
                    {"problem_id": f"존재하지 않는 problem_id입니다: {raw_id}"}
                )
            attrs["problem"] = problem
        attrs.pop("problem_id", None)
        from .models import ProblemPublication
        from .platform_permissions import is_manager

        if (
            not is_manager(self.context["request"].user)
            and ProblemPublication.objects.filter(problem=attrs["problem"])
            .exclude(status="published")
            .exists()
        ):
            raise serializers.ValidationError(
                "공개된 문제만 일반 학습으로 제출할 수 있습니다."
            )
        return attrs

    def create(self, validated_data):
        from .models import AssignmentRecipient
        from .services.assignments import released

        problem = validated_data["problem"]
        for recipient in (
            AssignmentRecipient.objects.filter(
                student__user=self.context["request"].user,
                assignment__items__problem=problem,
            )
            .select_related("assignment")
            .distinct()
        ):
            if not released(recipient) or (
                recipient.submitted_at is None
                and recipient.assignment.status != "cancelled"
            ):
                raise serializers.ValidationError(
                    "이 문제는 배정된 과제 화면에서 제출해 주세요."
                )
        return Attempt.objects.create(
            user=self.context["request"].user, **validated_data
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["problem_id"] = instance.problem.problem_id
        return data


class MasterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mastery
        fields = (
            "id",
            "concept",
            "tag_type",
            "score",
            "attempt_count",
            "correct_count",
            "last_practiced_at",
            "updated_at",
        )


class ProblemTaggingSerializer(serializers.ModelSerializer):
    problem_id = serializers.CharField(source="problem.problem_id", read_only=True)
    language = serializers.CharField(source="problem.language", read_only=True)
    problem_title = serializers.SerializerMethodField()
    reviewed_by_username = serializers.CharField(
        source="reviewed_by.username", read_only=True, default=None
    )
    effective_concepts = serializers.ListField(read_only=True)
    effective_skills = serializers.ListField(read_only=True)

    class Meta:
        from .models import ProblemTagging

        model = ProblemTagging
        fields = (
            "id",
            "problem",
            "problem_id",
            "language",
            "problem_title",
            "auto_concepts",
            "auto_skills",
            "rule_version",
            "source",
            "confidence",
            "review_status",
            "reviewed_concepts",
            "reviewed_skills",
            "effective_concepts",
            "effective_skills",
            "reviewed_by_username",
            "reviewed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "problem",
            "auto_concepts",
            "auto_skills",
            "rule_version",
            "source",
            "confidence",
            "created_at",
            "updated_at",
        )

    def get_problem_title(self, obj) -> str:
        metadata = obj.problem.semantic_data.get("metadata", {})
        return metadata.get("title") or obj.problem.problem_id
