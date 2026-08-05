from django.urls import path

from .views import (
    AnonymousSessionView,
    AttemptsView,
    DailySummaryView,
    MasteriesView,
    ReviewQueueView,
    TutorMessagesView,
)

urlpatterns = [
    path("auth/anonymous-session", AnonymousSessionView.as_view()),
    path("learning/attempts", AttemptsView.as_view()),
    path("learning/daily-summary", DailySummaryView.as_view()),
    path("learning/masteries", MasteriesView.as_view()),
    path("learning/review-queue", ReviewQueueView.as_view()),
    path("tutor/messages", TutorMessagesView.as_view()),
]
