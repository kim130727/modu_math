from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from .models import Attempt, Mastery, Problem


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password")
        read_only_fields = ("id",)

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


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
        return f"examples/problems/{obj.language}"


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
        return attrs

    def create(self, validated_data):
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
