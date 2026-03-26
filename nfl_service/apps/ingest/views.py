"""Views for ingestion API endpoints."""

import structlog
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ingest.serializers import (
    IngestionResultSerializer,
    IngestInjuriesRequestSerializer,
    IngestNewsRequestSerializer,
    IngestScoreboardRequestSerializer,
    IngestTeamsRequestSerializer,
    IngestTransactionsRequestSerializer,
)
from apps.ingest.services import (
    InjuryIngestionService,
    NewsIngestionService,
    ScoreboardIngestionService,
    TeamIngestionService,
    TransactionIngestionService,
)

logger = structlog.get_logger(__name__)


class IngestScoreboardView(APIView):
    """Endpoint for ingesting scoreboard data from nfl."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest scoreboard data",
        description=(
            "Fetch scoreboard data from nfl for a specific sport, league, and date, "
            "then upsert the events and competitors into the database."
        ),
        request=IngestScoreboardRequestSerializer,
        responses={
            200: IngestionResultSerializer,
            400: {"description": "Invalid request data"},
            502: {"description": "nfl API error"},
        },
    )
    def post(self, request: Request) -> Response:
        """Ingest scoreboard data from nfl."""
        serializer = IngestScoreboardRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sport = serializer.validated_data["sport"]
        league = serializer.validated_data["league"]
        date = serializer.validated_data.get("date")

        logger.info("scoreboard_ingestion_requested", sport=sport, league=league, date=date)

        service = ScoreboardIngestionService()
        result = service.ingest_scoreboard(sport, league, date)
        return Response(IngestionResultSerializer(result.to_dict()).data, status=status.HTTP_200_OK)


class IngestTeamsView(APIView):
    """Endpoint for ingesting team data from nfl."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest teams data",
        description=(
            "Fetch all teams from nfl for a specific sport and league, "
            "then upsert them into the database."
        ),
        request=IngestTeamsRequestSerializer,
        responses={
            200: IngestionResultSerializer,
            400: {"description": "Invalid request data"},
            502: {"description": "nfl API error"},
        },
    )
    def post(self, request: Request) -> Response:
        """Ingest teams data from nfl."""
        serializer = IngestTeamsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sport = serializer.validated_data["sport"]
        league = serializer.validated_data["league"]

        logger.info("teams_ingestion_requested", sport=sport, league=league)

        service = TeamIngestionService()
        result = service.ingest_teams(sport, league)
        return Response(IngestionResultSerializer(result.to_dict()).data, status=status.HTTP_200_OK)


class IngestNewsView(APIView):
    """Endpoint for ingesting news articles from nfl."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest news articles",
        description=(
            "Fetch news articles from nfl for a specific sport and league, "
            "then upsert them into the database."
        ),
        request=IngestNewsRequestSerializer,
        responses={
            200: IngestionResultSerializer,
            400: {"description": "Invalid request data"},
            502: {"description": "nfl API error"},
        },
    )
    def post(self, request: Request) -> Response:
        """Ingest news articles from nfl."""
        serializer = IngestNewsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sport = serializer.validated_data["sport"]
        league = serializer.validated_data["league"]
        limit = serializer.validated_data.get("limit", 50)

        logger.info("news_ingestion_requested", sport=sport, league=league, limit=limit)

        service = NewsIngestionService()
        result = service.ingest_news(sport, league, limit=limit)
        return Response(IngestionResultSerializer(result.to_dict()).data, status=status.HTTP_200_OK)


class IngestInjuriesView(APIView):
    """Endpoint for ingesting league injury reports from nfl."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest injury report",
        description=(
            "Fetch the current league injury report from nfl and refresh the database snapshot. "
            "This is a full replacement — all prior entries for the league are deleted then re-inserted."
        ),
        request=IngestInjuriesRequestSerializer,
        responses={
            200: IngestionResultSerializer,
            400: {"description": "Invalid request data"},
            502: {"description": "nfl API error"},
        },
    )
    def post(self, request: Request) -> Response:
        """Ingest injury report from nfl."""
        serializer = IngestInjuriesRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sport = serializer.validated_data["sport"]
        league = serializer.validated_data["league"]

        logger.info("injuries_ingestion_requested", sport=sport, league=league)

        service = InjuryIngestionService()
        result = service.ingest_injuries(sport, league)
        return Response(IngestionResultSerializer(result.to_dict()).data, status=status.HTTP_200_OK)


class IngestTransactionsView(APIView):
    """Endpoint for ingesting league transactions from nfl."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest transactions",
        description=(
            "Fetch the latest transactions from nfl for a specific sport and league, "
            "then upsert them into the database."
        ),
        request=IngestTransactionsRequestSerializer,
        responses={
            200: IngestionResultSerializer,
            400: {"description": "Invalid request data"},
            502: {"description": "nfl API error"},
        },
    )
    def post(self, request: Request) -> Response:
        """Ingest transactions from nfl."""
        serializer = IngestTransactionsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sport = serializer.validated_data["sport"]
        league = serializer.validated_data["league"]

        logger.info("transactions_ingestion_requested", sport=sport, league=league)

        service = TransactionIngestionService()
        result = service.ingest_transactions(sport, league)
        return Response(IngestionResultSerializer(result.to_dict()).data, status=status.HTTP_200_OK)
