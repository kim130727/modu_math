from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AttemptViewSet,
    LoginView,
    MasteryViewSet,
    ProblemViewSet,
    RegisterView,
)

router = DefaultRouter()
router.register("problems", ProblemViewSet, basename="problem")
router.register("attempts", AttemptViewSet, basename="attempt")
router.register("masteries", MasteryViewSet, basename="mastery")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("", include(router.urls)),
]
