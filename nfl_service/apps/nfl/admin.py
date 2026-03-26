"""Django admin configuration for nfl models."""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from apps.nfl.models import (
    Athlete,
    AthleteSeasonStats,
    Competitor,
    Event,
    Injury,
    League,
    NewsArticle,
    Sport,
    Team,
    Transaction,
    Venue,
)


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "league_count", "created_at"]
    search_fields = ["name", "slug"]
    readonly_fields = ["created_at", "updated_at"]

    def league_count(self, obj: Sport) -> int:
        return obj.leagues.count()

    league_count.short_description = "Leagues"  # type: ignore[attr-defined]


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ["name", "abbreviation", "sport", "team_count", "created_at"]
    list_filter = ["sport"]
    search_fields = ["name", "slug", "abbreviation"]
    readonly_fields = ["created_at", "updated_at"]

    def team_count(self, obj: League) -> int:
        return obj.teams.count()

    team_count.short_description = "Teams"  # type: ignore[attr-defined]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["display_name", "abbreviation", "league", "nfl_id", "is_active", "color_preview"]
    list_filter = ["league", "is_active", "is_all_star"]
    search_fields = ["display_name", "abbreviation", "nfl_id", "slug"]
    readonly_fields = ["created_at", "updated_at", "logo_preview"]

    def color_preview(self, obj: Team) -> str:
        if obj.color:
            return format_html(
                '<span style="background-color: #{0}; padding: 2px 10px; '
                'border-radius: 3px; color: white;">{0}</span>',
                obj.color,
            )
        return "-"

    color_preview.short_description = "Color"  # type: ignore[attr-defined]

    def logo_preview(self, obj: Team) -> str:
        logo_url = obj.primary_logo
        if logo_url:
            return format_html(
                '<img src="{0}" style="max-height: 100px; max-width: 100px;" />',
                logo_url,
            )
        return "-"

    logo_preview.short_description = "Logo"  # type: ignore[attr-defined]


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "city", "state", "is_indoor", "capacity", "nfl_id"]
    list_filter = ["is_indoor", "state", "country"]
    search_fields = ["name", "city", "nfl_id"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["short_name", "league", "date", "status", "venue", "nfl_id"]
    list_filter = ["league", "status", "season_year", "season_type"]
    search_fields = ["name", "short_name", "nfl_id"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "date"

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("league", "venue")


@admin.register(Competitor)
class CompetitorAdmin(admin.ModelAdmin):
    list_display = ["team", "event", "home_away", "score", "winner"]
    list_filter = ["home_away", "winner", "event__league"]
    search_fields = ["team__display_name", "event__name"]
    readonly_fields = ["created_at", "updated_at"]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("team", "event")


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ["display_name", "team", "position", "jersey", "is_active", "nfl_id"]
    list_filter = ["is_active", "team__league", "position"]
    search_fields = ["full_name", "display_name", "nfl_id"]
    readonly_fields = ["created_at", "updated_at", "headshot_preview"]

    def headshot_preview(self, obj: Athlete) -> str:
        if obj.headshot:
            return format_html(
                '<img src="{0}" style="max-height: 100px; max-width: 100px;" />',
                obj.headshot,
            )
        return "-"

    headshot_preview.short_description = "Headshot"  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# New model admins — added in audit expansion
# ---------------------------------------------------------------------------


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    """Admin for NewsArticle model."""

    list_display = ["headline_truncated", "type", "league", "published", "created_at"]
    list_filter = ["type", "league__sport", "league"]
    search_fields = ["headline", "description", "nfl_id"]
    readonly_fields = ["created_at", "updated_at", "thumbnail_preview"]
    date_hierarchy = "published"

    def headline_truncated(self, obj: NewsArticle) -> str:
        return obj.headline[:60] + "…" if len(obj.headline) > 60 else obj.headline

    headline_truncated.short_description = "Headline"  # type: ignore[attr-defined]

    def thumbnail_preview(self, obj: NewsArticle) -> str:
        url = obj.thumbnail
        if url:
            return format_html('<img src="{0}" style="max-height: 80px;" />', url)
        return "-"

    thumbnail_preview.short_description = "Thumbnail"  # type: ignore[attr-defined]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("league", "league__sport")


@admin.register(Injury)
class InjuryAdmin(admin.ModelAdmin):
    """Admin for Injury model."""

    list_display = [
        "athlete_name",
        "position",
        "status",
        "injury_type",
        "team",
        "league",
        "updated_at",
    ]
    list_filter = ["status", "league__sport", "league"]
    search_fields = ["athlete_name", "injury_type", "description", "athlete_nfl_id"]
    readonly_fields = ["created_at", "updated_at"]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("league", "league__sport", "team")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin for Transaction model."""

    list_display = ["description_truncated", "type", "athlete_name", "team", "league", "date"]
    list_filter = ["type", "league__sport", "league"]
    search_fields = ["description", "athlete_name", "nfl_id", "athlete_nfl_id"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "date"

    def description_truncated(self, obj: Transaction) -> str:
        return obj.description[:60] + "…" if len(obj.description) > 60 else obj.description

    description_truncated.short_description = "Description"  # type: ignore[attr-defined]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("league", "league__sport", "team")


@admin.register(AthleteSeasonStats)
class AthleteSeasonStatsAdmin(admin.ModelAdmin):
    """Admin for AthleteSeasonStats model."""

    list_display = [
        "athlete_name",
        "athlete_nfl_id",
        "league",
        "season_year",
        "season_type",
        "updated_at",
    ]
    list_filter = ["season_year", "season_type", "league__sport", "league"]
    search_fields = ["athlete_name", "athlete_nfl_id"]
    readonly_fields = ["created_at", "updated_at"]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return (
            super().get_queryset(request).select_related("league", "league__sport", "athlete")
        )
