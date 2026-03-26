"""Serializers for nfl data models."""

from rest_framework import serializers

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


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ["id", "slug", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class LeagueSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    sport_slug = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = League
        fields = ["id", "slug", "name", "abbreviation", "sport", "sport_slug", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class LeagueMinimalSerializer(serializers.ModelSerializer):
    sport_slug = serializers.CharField(source="sport.slug", read_only=True)

    class Meta:
        model = League
        fields = ["id", "slug", "name", "abbreviation", "sport_slug"]


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            "id", "nfl_id", "name", "city", "state", "country",
            "is_indoor", "capacity", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TeamSerializer(serializers.ModelSerializer):
    league = LeagueMinimalSerializer(read_only=True)
    primary_logo = serializers.CharField(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id", "nfl_id", "uid", "slug", "abbreviation", "display_name",
            "short_display_name", "name", "nickname", "location", "color",
            "alternate_color", "is_active", "is_all_star", "logos", "primary_logo",
            "league", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TeamListSerializer(serializers.ModelSerializer):
    league_slug = serializers.CharField(source="league.slug", read_only=True)
    sport_slug = serializers.CharField(source="league.sport.slug", read_only=True)
    primary_logo = serializers.CharField(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id", "nfl_id", "abbreviation", "display_name", "short_display_name",
            "location", "color", "primary_logo", "league_slug", "sport_slug", "is_active",
        ]


class TeamMinimalSerializer(serializers.ModelSerializer):
    primary_logo = serializers.CharField(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id", "nfl_id", "abbreviation", "display_name",
            "short_display_name", "location", "color", "primary_logo",
        ]


class CompetitorSerializer(serializers.ModelSerializer):
    team = TeamMinimalSerializer(read_only=True)
    score_int = serializers.IntegerField(read_only=True)

    class Meta:
        model = Competitor
        fields = [
            "id", "team", "home_away", "score", "score_int",
            "winner", "line_scores", "records", "statistics", "leaders", "order",
        ]


class EventSerializer(serializers.ModelSerializer):
    league = LeagueMinimalSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    competitors = CompetitorSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "nfl_id", "uid", "date", "name", "short_name",
            "season_year", "season_type", "season_slug", "week",
            "status", "status_detail", "clock", "period", "attendance",
            "broadcasts", "links", "league", "venue", "competitors",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class EventListSerializer(serializers.ModelSerializer):
    league_slug = serializers.CharField(source="league.slug", read_only=True)
    sport_slug = serializers.CharField(source="league.sport.slug", read_only=True)
    venue_name = serializers.CharField(source="venue.name", read_only=True, allow_null=True)
    competitors = CompetitorSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "nfl_id", "date", "name", "short_name", "status", "status_detail",
            "league_slug", "sport_slug", "venue_name", "competitors",
        ]


class AthleteSerializer(serializers.ModelSerializer):
    team = TeamMinimalSerializer(read_only=True)

    class Meta:
        model = Athlete
        fields = [
            "id", "nfl_id", "uid", "first_name", "last_name", "full_name",
            "display_name", "short_name", "position", "position_abbreviation",
            "jersey", "is_active", "height", "weight", "age", "birth_date",
            "birth_place", "headshot", "team", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ---------------------------------------------------------------------------
# New model serializers — added in audit expansion
# ---------------------------------------------------------------------------


class NewsArticleSerializer(serializers.ModelSerializer):
    """Serializer for NewsArticle model."""

    league_slug = serializers.CharField(source="league.slug", read_only=True, allow_null=True)
    sport_slug = serializers.CharField(source="league.sport.slug", read_only=True, allow_null=True)
    thumbnail = serializers.CharField(read_only=True)

    class Meta:
        model = NewsArticle
        fields = [
            "id", "nfl_id", "headline", "description", "published",
            "last_modified", "type", "categories", "images", "links",
            "thumbnail", "league_slug", "sport_slug", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class NewsArticleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for news article lists."""

    league_slug = serializers.CharField(source="league.slug", read_only=True, allow_null=True)
    sport_slug = serializers.CharField(source="league.sport.slug", read_only=True, allow_null=True)
    thumbnail = serializers.CharField(read_only=True)

    class Meta:
        model = NewsArticle
        fields = [
            "id", "nfl_id", "headline", "description", "published",
            "type", "thumbnail", "league_slug", "sport_slug",
        ]


class InjurySerializer(serializers.ModelSerializer):
    """Serializer for Injury model."""

    league_slug = serializers.CharField(source="league.slug", read_only=True)
    sport_slug = serializers.CharField(source="league.sport.slug", read_only=True)
    team_abbreviation = serializers.CharField(
        source="team.abbreviation", read_only=True, allow_null=True
    )

    class Meta:
        model = Injury
        fields = [
            "id", "athlete_nfl_id", "athlete_name", "position",
            "status", "status_display", "description", "injury_type",
            "injury_date", "return_date",
            "league_slug", "sport_slug", "team_abbreviation",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""

    league_slug = serializers.CharField(source="league.slug", read_only=True)
    sport_slug = serializers.CharField(source="league.sport.slug", read_only=True)
    team_abbreviation = serializers.CharField(
        source="team.abbreviation", read_only=True, allow_null=True
    )

    class Meta:
        model = Transaction
        fields = [
            "id", "nfl_id", "date", "description", "type",
            "athlete_name", "athlete_nfl_id",
            "league_slug", "sport_slug", "team_abbreviation",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class AthleteSeasonStatsSerializer(serializers.ModelSerializer):
    """Serializer for AthleteSeasonStats model."""

    league_slug = serializers.CharField(source="league.slug", read_only=True)
    sport_slug = serializers.CharField(source="league.sport.slug", read_only=True)

    class Meta:
        model = AthleteSeasonStats
        fields = [
            "id", "athlete_nfl_id", "athlete_name",
            "season_year", "season_type", "stats",
            "league_slug", "sport_slug",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
