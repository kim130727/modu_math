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
from .platform_views import (
    AdminUserViewSet,
    AssignmentViewSet,
    ClassroomViewSet,
    CurrentUserView,
    EditorSessionView,
    JoinClassView,
    LogoutView,
    ProblemSetViewSet,
    StudentAssignmentViewSet,
    StudentViewSet,
    TeacherDashboardView,
)

router.register("classes", ClassroomViewSet, basename="classroom")
router.register("admin/users", AdminUserViewSet, basename="admin-user")
router.register("students", StudentViewSet, basename="student")
router.register("problem-sets", ProblemSetViewSet, basename="problem-set")
router.register("assignments", AssignmentViewSet, basename="assignment")
router.register(
    "student/assignments", StudentAssignmentViewSet, basename="student-assignment"
)
router.register("problems", ProblemViewSet, basename="problem")
router.register("attempts", AttemptViewSet, basename="attempt")
router.register("masteries", MasteryViewSet, basename="mastery")
router.register(
    "admin/problem-tags", ProblemTaggingViewSet, basename="admin-problem-tag"
)

urlpatterns = [
    path("auth/editor-session/", EditorSessionView.as_view(), name="editor-session"),
    path("auth/me/", CurrentUserView.as_view(), name="current-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("student/join-class/", JoinClassView.as_view(), name="join-class"),
    path(
        "teacher/dashboard/", TeacherDashboardView.as_view(), name="teacher-dashboard"
    ),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path(
        "diagnostics/summary/",
        DiagnosticSummaryView.as_view(),
        name="diagnostic-summary",
    ),
    path(
        "diagnostics/concepts/",
        DiagnosticConceptsView.as_view(),
        name="diagnostic-concepts",
    ),
    path(
        "diagnostics/skills/", DiagnosticSkillsView.as_view(), name="diagnostic-skills"
    ),
    path(
        "diagnostics/history/",
        DiagnosticHistoryView.as_view(),
        name="diagnostic-history",
    ),
    path("recommendations/", RecommendationsView.as_view(), name="recommendations"),
    path("", include(router.urls)),
]
