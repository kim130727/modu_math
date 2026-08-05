from datetime import datetime, timezone

from rest_framework import serializers


ERROR_CATEGORIES = (
    "understanding_target",
    "understanding_given",
    "planning_concept",
    "planning_operation",
    "execution_calculation",
    "execution_representation",
    "review_condition",
    "review_unit",
    "none",
)

TUTOR_ACTIONS = ("hint", "next_question", "respond", "review_answer")
REPLY_TYPES = ("greeting", "hint", "question", "correct", "retry")


class AnonymousSessionSerializer(serializers.Serializer):
    deviceId = serializers.CharField(max_length=128)
    grade = serializers.IntegerField(min_value=1, max_value=12)
    displayName = serializers.CharField(
        max_length=40,
        required=False,
        allow_blank=True,
        default="Student",
    )


class AttemptSerializer(serializers.Serializer):
    problemId = serializers.CharField(max_length=128)
    unit = serializers.CharField(max_length=120)
    answer = serializers.CharField(max_length=500, allow_blank=True)
    isCorrect = serializers.BooleanField()
    hintLevelUsed = serializers.IntegerField(min_value=0, default=0)
    timeSpentSeconds = serializers.IntegerField(min_value=0, default=0)
    errorCategory = serializers.ChoiceField(choices=ERROR_CATEGORIES, default="none")
    answeredAt = serializers.DateTimeField(required=False)

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        value["problem_id"] = value.pop("problemId")
        value["is_correct"] = value.pop("isCorrect")
        value["hint_level_used"] = value.pop("hintLevelUsed")
        value["time_spent_seconds"] = value.pop("timeSpentSeconds")
        value["error_category"] = value.pop("errorCategory")
        value["answered_at"] = value.pop("answeredAt", datetime.now(timezone.utc))
        return value


class TutorMessageSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=("tutor", "student"))
    text = serializers.CharField(allow_blank=True, max_length=2000)
    replyType = serializers.ChoiceField(
        choices=REPLY_TYPES,
        required=False,
        allow_null=True,
    )
    createdAt = serializers.DateTimeField(required=False)


class TutorProblemSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=128)
    grade = serializers.IntegerField(min_value=1, max_value=12)
    subject = serializers.CharField(max_length=40)
    unit = serializers.CharField(max_length=120)
    type = serializers.CharField(max_length=80)
    title = serializers.CharField(max_length=160, allow_blank=True)
    prompt = serializers.CharField(max_length=4000, allow_blank=True)
    choices = serializers.ListField(
        child=serializers.CharField(max_length=400),
        required=False,
        default=list,
    )
    correctAnswer = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        write_only=True,
    )
    answerMap = serializers.DictField(required=False, default=dict, write_only=True)
    semantic = serializers.DictField(required=False, default=dict, write_only=True)
    solvable = serializers.DictField(required=False, default=dict, write_only=True)


class TutorRequestSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=TUTOR_ACTIONS)
    problem = TutorProblemSerializer()
    messages = TutorMessageSerializer(many=True, required=False, default=list)
    hintLevel = serializers.IntegerField(min_value=0, required=False)
    stepIndex = serializers.IntegerField(min_value=0, required=False)
    message = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    answer = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def validate(self, attrs):
        action = attrs["action"]
        required_by_action = {
            "hint": ("hintLevel",),
            "next_question": ("stepIndex",),
            "respond": ("message", "stepIndex"),
            "review_answer": ("answer",),
        }
        missing = [name for name in required_by_action[action] if name not in attrs]
        if missing:
            raise serializers.ValidationError(
                {name: ["This field is required for this action."] for name in missing}
            )
        return attrs
