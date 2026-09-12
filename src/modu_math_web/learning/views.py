from __future__ import annotations

from django.utils import timezone
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
        queryset = Mastery.objects.filter(user=self.request.user)
        tag_type = self.request.query_params.get("tag_type")
        if tag_type:
            queryset = queryset.filter(tag_type=tag_type)
        return queryset


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
