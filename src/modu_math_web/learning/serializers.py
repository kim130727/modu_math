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
            "updated_at",
        )


class ProblemDetailSerializer(serializers.ModelSerializer):
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
            "answer",
            "semantic_data",
            "solvable_data",
            "layout_data",
            "renderer_data",
            "updated_at",
        )


class AttemptSerializer(serializers.ModelSerializer):
    problem_id = serializers.CharField(source="problem.problem_id", read_only=True)
    language = serializers.CharField(source="problem.language", read_only=True)

    class Meta:
        model = Attempt
        fields = (
            "id",
            "problem",
            "problem_id",
            "language",
            "submitted_answer",
            "is_correct",
            "elapsed_ms",
            "hint_count",
            "retry_count",
            "events",
            "created_at",
        )
        read_only_fields = ("id", "is_correct", "created_at")

    def validate_events(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("events는 배열이어야 합니다.")
        return value

    def create(self, validated_data):
        return Attempt.objects.create(
            user=self.context["request"].user, **validated_data
        )


class MasterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mastery
        fields = (
            "id",
            "concept",
            "score",
            "attempt_count",
            "correct_count",
            "last_practiced_at",
            "updated_at",
        )
