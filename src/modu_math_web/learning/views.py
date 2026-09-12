from rest_framework import mixins, permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Attempt, Mastery, Problem
from .serializers import (
    AttemptSerializer,
    LoginSerializer,
    MasterySerializer,
    ProblemDetailSerializer,
    ProblemListSerializer,
    RegisterSerializer,
)


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
                },
            }
        )


class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Problem.objects.all()

    def get_serializer_class(self):
        return (
            ProblemListSerializer if self.action == "list" else ProblemDetailSerializer
        )

    def get_queryset(self):
        queryset = super().get_queryset()
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
        return queryset


class AttemptViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AttemptSerializer

    def get_queryset(self):
        queryset = Attempt.objects.filter(user=self.request.user).select_related(
            "problem"
        )
        problem_id = self.request.query_params.get("problem_id")
        if problem_id:
            queryset = queryset.filter(problem__problem_id=problem_id)
        return queryset


class MasteryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MasterySerializer

    def get_queryset(self):
        return Mastery.objects.filter(user=self.request.user)
