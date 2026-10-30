from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
    Assignment,
    Classroom,
    Enrollment,
    Problem,
    ProblemPublication,
    ProblemSet,
)


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("id", "name", "teacher", "invite_code", "archived")
        read_only_fields = ("id", "teacher", "invite_code")


class EnrollmentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="student.user.username", read_only=True)

    class Meta:
        model = Enrollment
        fields = ("id", "classroom", "student", "username", "status")
        read_only_fields = ("id", "classroom", "student", "username")


class StudentCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)

    def validate_username(self, value):
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용 중인 아이디입니다.")
        get_user_model()._meta.get_field("username").run_validators(value)
        return value


class ProblemSetSerializer(serializers.ModelSerializer):
    problem_ids = serializers.PrimaryKeyRelatedField(
        queryset=Problem.objects.all(),
        many=True,
        write_only=True,
        allow_empty=False,
        required=False,
    )
    items = serializers.SerializerMethodField()

    class Meta:
        model = ProblemSet
        fields = (
            "id",
            "title",
            "description",
            "version",
            "problem_ids",
            "items",
            "updated_at",
        )
        read_only_fields = ("id", "version", "updated_at")

    def get_items(self, obj):
        return [
            {"problem": item.problem_id, "position": item.position}
            for item in obj.items.all()
        ]

    def validate(self, attrs):
        if self.instance is None and not attrs.get("problem_ids"):
            raise serializers.ValidationError({"problem_ids": "문제를 선택해 주세요."})
        if len(attrs.get("problem_ids", [])) > 200:
            raise serializers.ValidationError("문제집당 최대 200문항입니다.")
        return attrs


class AssignmentCreateSerializer(serializers.ModelSerializer):
    student_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
        allow_empty=True,
        max_length=500,
    )
    class_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
        allow_empty=True,
        max_length=100,
    )

    class Meta:
        model = Assignment
        fields = (
            "id",
            "problem_set",
            "title",
            "starts_at",
            "due_at",
            "max_attempts",
            "release_policy",
            "student_ids",
            "class_ids",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        if not attrs.get("student_ids") and not attrs.get("class_ids"):
            raise serializers.ValidationError("학생 또는 학급을 선택해 주세요.")
        if (
            attrs.get("starts_at")
            and attrs.get("due_at")
            and attrs["starts_at"] >= attrs["due_at"]
        ):
            raise serializers.ValidationError("마감일은 시작일보다 늦어야 합니다.")
        if attrs.get("release_policy") == "after_due" and not attrs.get("due_at"):
            raise serializers.ValidationError("마감 후 공개에는 마감일이 필요합니다.")
        return attrs


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemPublication
        fields = ("status", "difficulty", "updated_at")
        read_only_fields = ("updated_at",)


class AnswerSubmissionSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(min_value=1)
    answer = serializers.JSONField()
    submission_key = serializers.CharField(max_length=64)
    elapsed_ms = serializers.IntegerField(min_value=0, max_value=86400000, default=0)
    hint_count = serializers.IntegerField(min_value=0, max_value=1000, default=0)


class DraftSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(min_value=1)
    answer = serializers.JSONField(allow_null=True)


class EnrollmentRequestSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(min_value=1)


class JoinSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=64)


class ReviewSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField(min_value=1)
    title = serializers.CharField(max_length=160, default="오답 복습")


class AssignmentStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=("active", "closed", "cancelled"))


class UserAccessSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=("student", "teacher", "admin"), required=False
    )
    is_active = serializers.BooleanField(required=False)
