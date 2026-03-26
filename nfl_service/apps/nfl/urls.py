"""URL configuration for nfl app."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.nfl.views import (
    AthleteSeasonStatsViewSet,
    EventViewSet,
    InjuryViewSet,
    LeagueViewSet,
    NewsArticleViewSet,
    SportViewSet,
    TeamViewSet,
    TransactionViewSet,
)

app_name = "nfl"

router = DefaultRouter()
router.register(r"sports", SportViewSet, basename="sport")
router.register(r"leagues", LeagueViewSet, basename="league")
router.register(r"teams", TeamViewSet, basename="team")
router.register(r"events", EventViewSet, basename="event")
router.register(r"news", NewsArticleViewSet, basename="news")
router.register(r"injuries", InjuryViewSet, basename="injury")
router.register(r"transactions", TransactionViewSet, basename="transaction")
router.register(r"athlete-stats", AthleteSeasonStatsViewSet, basename="athlete-stats")

urlpatterns = [
    path("", include(router.urls)),
]
