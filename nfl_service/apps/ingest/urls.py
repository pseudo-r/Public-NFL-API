"""URL configuration for ingest app."""

from django.urls import path

from apps.ingest.views import (
    IngestInjuriesView,
    IngestNewsView,
    IngestScoreboardView,
    IngestTeamsView,
    IngestTransactionsView,
)

app_name = "ingest"

urlpatterns = [
    path("scoreboard/", IngestScoreboardView.as_view(), name="ingest-scoreboard"),
    path("teams/", IngestTeamsView.as_view(), name="ingest-teams"),
    path("news/", IngestNewsView.as_view(), name="ingest-news"),
    path("injuries/", IngestInjuriesView.as_view(), name="ingest-injuries"),
    path("transactions/", IngestTransactionsView.as_view(), name="ingest-transactions"),
]
