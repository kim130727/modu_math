from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AttemptViewSet,
    DiagnosticConceptsView,
    DiagnosticHistoryView,
    DiagnosticSkillsView,
    DiagnosticSummaryView,
    LoginView,
    MasteryViewSet,
    ProblemTaggingViewSet,
    ProblemViewSet,
    RecommendationsView,
    RegisterView,
)

router = DefaultRouter()
router.register("problems", ProblemViewSet, basename="problem")
router.register("attempts", AttemptViewSet, basename="attempt")
router.register("masteries", MasteryViewSet, basename="mastery")
router.register("admin/problem-tags", ProblemTaggingViewSet, basename="admin-problem-tag")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("diagnostics/summary/", DiagnosticSummaryView.as_view(), name="diagnostic-summary"),
    path("diagnostics/concepts/", DiagnosticConceptsView.as_view(), name="diagnostic-concepts"),
    path("diagnostics/skills/", DiagnosticSkillsView.as_view(), name="diagnostic-skills"),
    path("diagnostics/history/", DiagnosticHistoryView.as_view(), name="diagnostic-history"),
    path("recommendations/", RecommendationsView.as_view(), name="recommendations"),
    path("", include(router.urls)),
]
