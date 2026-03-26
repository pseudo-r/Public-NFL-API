"""Celery tasks for nfl data ingestion.

All tasks are idempotent — safe to retry or run concurrently for
different sport/league combinations.
"""

from __future__ import annotations

import structlog
from celery import shared_task

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# League configuration — keep in sync with ingest_all_teams.py
# ---------------------------------------------------------------------------

ALL_LEAGUES_CONFIG: list[tuple[str, str]] = [
    # Football
    ("football", "nfl"),
    ("football", "college-football"),
    ("football", "cfl"),
    ("football", "ufl"),
    ("football", "xfl"),
    # Basketball
    ("basketball", "nba"),
    ("basketball", "wnba"),
    ("basketball", "nba-development"),
    ("basketball", "mens-college-basketball"),
    ("basketball", "womens-college-basketball"),
    ("basketball", "nbl"),
    # Baseball
    ("baseball", "mlb"),
    ("baseball", "college-baseball"),
    # Hockey
    ("hockey", "nhl"),
    ("hockey", "mens-college-hockey"),
    ("hockey", "womens-college-hockey"),
    # Soccer — major leagues only for Celery (performance)
    ("soccer", "eng.1"),
    ("soccer", "esp.1"),
    ("soccer", "ger.1"),
    ("soccer", "ita.1"),
    ("soccer", "fra.1"),
    ("soccer", "usa.1"),
    ("soccer", "eng.2"),
    ("soccer", "uefa.champions"),
    # Golf
    ("golf", "pga"),
    ("golf", "lpga"),
    ("golf", "eur"),
    ("golf", "liv"),
    # Racing
    ("racing", "f1"),
    ("racing", "irl"),
    ("racing", "nascar-premier"),
    ("racing", "nascar-secondary"),
    ("racing", "nascar-truck"),
    # Tennis
    ("tennis", "atp"),
    ("tennis", "wta"),
    # MMA
    ("mma", "ufc"),
    ("mma", "bellator"),
    # Rugby
    ("rugby", "premiership"),
    ("rugby", "rugby-union-super-rugby"),
    ("rugby", "internationals"),
    # Rugby League
    ("rugby-league", "nrl"),
    # Lacrosse
    ("lacrosse", "pll"),
    ("lacrosse", "nll"),
    ("lacrosse", "mens-college-lacrosse"),
    ("lacrosse", "womens-college-lacrosse"),
]


# ---------------------------------------------------------------------------
# Scoreboard tasks
# ---------------------------------------------------------------------------


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_scoreboard_task(self, sport: str, league: str, date: str | None = None) -> dict:
    """Ingest scoreboard data for a single sport/league."""
    from apps.ingest.services import ScoreboardIngestionService

    try:
        service = ScoreboardIngestionService()
        result = service.ingest_scoreboard(sport, league, date)
        logger.info(
            "scoreboard_task_completed",
            sport=sport,
            league=league,
            date=date,
            created=result.created,
            updated=result.updated,
        )
        return result.to_dict()
    except Exception as exc:
        logger.error("scoreboard_task_failed", sport=sport, league=league, error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=2, default_retry_delay=120)
def refresh_all_scoreboards_task(self) -> dict:
    """Ingest today's scoreboard for every configured league."""
    total = {"created": 0, "updated": 0, "errors": 0}
    for sport, league in ALL_LEAGUES_CONFIG:
        try:
            refresh_scoreboard_task.delay(sport, league)
        except Exception as e:
            logger.error("refresh_all_scoreboards_dispatch_error", sport=sport, league=league, error=str(e))
            total["errors"] += 1
    return total


# ---------------------------------------------------------------------------
# Team tasks
# ---------------------------------------------------------------------------


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_teams_task(self, sport: str, league: str) -> dict:
    """Ingest team data for a single sport/league."""
    from apps.ingest.services import TeamIngestionService

    try:
        service = TeamIngestionService()
        result = service.ingest_teams(sport, league)
        logger.info("teams_task_completed", sport=sport, league=league, created=result.created)
        return result.to_dict()
    except Exception as exc:
        logger.error("teams_task_failed", sport=sport, league=league, error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=2, default_retry_delay=120)
def refresh_all_teams_task(self) -> dict:
    """Ingest teams for every configured league (weekly refresh)."""
    total = {"created": 0, "updated": 0, "errors": 0}
    for sport, league in ALL_LEAGUES_CONFIG:
        try:
            refresh_teams_task.delay(sport, league)
        except Exception as e:
            logger.error("refresh_all_teams_dispatch_error", sport=sport, league=league, error=str(e))
            total["errors"] += 1
    return total


# ---------------------------------------------------------------------------
# News tasks (NEW)
# ---------------------------------------------------------------------------


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_news_task(self, sport: str, league: str, limit: int = 50) -> dict:
    """Ingest news articles for a single sport/league."""
    from apps.ingest.services import NewsIngestionService

    try:
        service = NewsIngestionService()
        result = service.ingest_news(sport, league, limit=limit)
        logger.info(
            "news_task_completed",
            sport=sport,
            league=league,
            created=result.created,
            updated=result.updated,
        )
        return result.to_dict()
    except Exception as exc:
        logger.error("news_task_failed", sport=sport, league=league, error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=2, default_retry_delay=120)
def refresh_all_news_task(self) -> dict:
    """Ingest latest news for every configured league (runs every 30 min)."""
    total = {"created": 0, "updated": 0, "errors": 0}
    for sport, league in ALL_LEAGUES_CONFIG:
        try:
            refresh_news_task.delay(sport, league)
        except Exception as e:
            logger.error("refresh_all_news_dispatch_error", sport=sport, league=league, error=str(e))
            total["errors"] += 1
    return total


# ---------------------------------------------------------------------------
# Injury tasks (NEW)
# ---------------------------------------------------------------------------


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_injuries_task(self, sport: str, league: str) -> dict:
    """Refresh injury report for a single sport/league (full snapshot)."""
    from apps.ingest.services import InjuryIngestionService

    try:
        service = InjuryIngestionService()
        result = service.ingest_injuries(sport, league)
        logger.info(
            "injuries_task_completed",
            sport=sport,
            league=league,
            created=result.created,
        )
        return result.to_dict()
    except Exception as exc:
        logger.error("injuries_task_failed", sport=sport, league=league, error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=2, default_retry_delay=120)
def refresh_all_injuries_task(self) -> dict:
    """Refresh injury reports for every configured league (runs every 4 hours)."""
    total = {"created": 0, "errors": 0}
    for sport, league in ALL_LEAGUES_CONFIG:
        try:
            refresh_injuries_task.delay(sport, league)
        except Exception as e:
            logger.error("refresh_all_injuries_dispatch_error", sport=sport, league=league, error=str(e))
            total["errors"] += 1
    return total


# ---------------------------------------------------------------------------
# Transaction tasks (NEW)
# ---------------------------------------------------------------------------


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_transactions_task(self, sport: str, league: str) -> dict:
    """Ingest transactions for a single sport/league."""
    from apps.ingest.services import TransactionIngestionService

    try:
        service = TransactionIngestionService()
        result = service.ingest_transactions(sport, league)
        logger.info(
            "transactions_task_completed",
            sport=sport,
            league=league,
            created=result.created,
            updated=result.updated,
        )
        return result.to_dict()
    except Exception as exc:
        logger.error("transactions_task_failed", sport=sport, league=league, error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=2, default_retry_delay=120)
def refresh_all_transactions_task(self) -> dict:
    """Refresh transaction feeds for every configured league (runs every 6 hours)."""
    total = {"created": 0, "updated": 0, "errors": 0}
    for sport, league in ALL_LEAGUES_CONFIG:
        try:
            refresh_transactions_task.delay(sport, league)
        except Exception as e:
            logger.error(
                "refresh_all_transactions_dispatch_error",
                sport=sport,
                league=league,
                error=str(e),
            )
            total["errors"] += 1
    return total
