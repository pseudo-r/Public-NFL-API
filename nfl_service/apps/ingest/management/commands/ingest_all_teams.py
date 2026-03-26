"""Management command to ingest teams for all configured leagues."""

from django.core.management.base import BaseCommand, CommandError

from apps.ingest.services import TeamIngestionService

# All major leagues across all 17 sports
ALL_LEAGUES = [
    # Football
    ("football", "nfl"),
    ("football", "college-football"),
    ("football", "cfl"),
    ("football", "ufl"),
    ("football", "xfl"),
    # Basketball
    ("basketball", "nba"),
    ("basketball", "wnba"),
    ("basketball", "mens-college-basketball"),
    ("basketball", "womens-college-basketball"),
    ("basketball", "nba-development"),
    ("basketball", "nbl"),
    # Baseball
    ("baseball", "mlb"),
    ("baseball", "college-baseball"),
    # Hockey
    ("hockey", "nhl"),
    ("hockey", "mens-college-hockey"),
    ("hockey", "womens-college-hockey"),
    # Soccer — top leagues + major competitions
    ("soccer", "eng.1"),
    ("soccer", "usa.1"),
    ("soccer", "esp.1"),
    ("soccer", "ger.1"),
    ("soccer", "ita.1"),
    ("soccer", "fra.1"),
    ("soccer", "mex.1"),
    ("soccer", "uefa.champions"),
    ("soccer", "uefa.europa"),
    ("soccer", "usa.nwsl"),
    ("soccer", "eng.2"),
    # MMA
    ("mma", "ufc"),
    ("mma", "bellator"),
    # Golf
    ("golf", "pga"),
    ("golf", "lpga"),
    ("golf", "liv"),
    ("golf", "eur"),
    # Tennis
    ("tennis", "atp"),
    ("tennis", "wta"),
    # Racing
    ("racing", "f1"),
    ("racing", "irl"),
    ("racing", "nascar-premier"),
    ("racing", "nascar-secondary"),
    ("racing", "nascar-truck"),
    # Rugby Union (numeric IDs)
    ("rugby", "164205"),   # Rugby World Cup
    ("rugby", "180659"),   # Six Nations
    ("rugby", "267979"),   # Gallagher Premiership
    ("rugby", "242041"),   # Super Rugby Pacific
    ("rugby", "289262"),   # Major League Rugby
    # Rugby League
    ("rugby-league", "3"),
    # Lacrosse
    ("lacrosse", "pll"),
    ("lacrosse", "nll"),
    ("lacrosse", "mens-college-lacrosse"),
    ("lacrosse", "womens-college-lacrosse"),
    # Australian Football
    ("australian-football", "afl"),
]


class Command(BaseCommand):
    """Django management command to ingest teams for all supported leagues."""

    help = (
        "Ingest team data from nfl for all configured leagues. "
        "Use --sport to filter by sport or --dry-run to preview without ingesting."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--sport",
            type=str,
            default=None,
            help="Optional: filter to a single sport slug (e.g., basketball)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Print leagues that would be ingested without actually ingesting",
        )
        parser.add_argument(
            "--continue-on-error",
            action="store_true",
            default=True,
            help="Continue processing remaining leagues if one fails (default: True)",
        )

    def handle(self, *args, **options):
        sport_filter = options.get("sport")
        dry_run = options["dry_run"]
        continue_on_error = options["continue_on_error"]

        leagues = ALL_LEAGUES
        if sport_filter:
            leagues = [(s, league_slug) for s, league_slug in ALL_LEAGUES if s == sport_filter.lower()]
            if not leagues:
                raise CommandError(
                    f"No leagues configured for sport: {sport_filter}. "
                    f"Available sports: {sorted({s for s, _ in ALL_LEAGUES})}"
                )

        self.stdout.write(
            f"{'[DRY RUN] ' if dry_run else ''}Ingesting teams for "
            f"{len(leagues)} league(s)"
            + (f" (sport: {sport_filter})" if sport_filter else "")
        )

        if dry_run:
            for sport, league in leagues:
                self.stdout.write(f"  • {sport}/{league}")
            return

        total_created = 0
        total_updated = 0
        total_errors = 0
        failures = []

        for sport, league in leagues:
            self.stdout.write(f"  Ingesting {sport}/{league}...", ending="")

            try:
                service = TeamIngestionService()
                result = service.ingest_teams(sport, league)
                total_created += result.created
                total_updated += result.updated
                total_errors += result.errors

                status_str = (
                    self.style.SUCCESS(
                        f" ✓ created={result.created} updated={result.updated}"
                        + (f" errors={result.errors}" if result.errors else "")
                    )
                )
                self.stdout.write(status_str)

            except Exception as e:
                failure_msg = f" ✗ {e}"
                self.stdout.write(self.style.ERROR(failure_msg))
                failures.append(f"{sport}/{league}: {e}")
                if not continue_on_error:
                    raise CommandError(f"Stopped at {sport}/{league}: {e}") from e

        # Summary
        self.stdout.write("\n" + "─" * 50)
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Total: created={total_created} updated={total_updated} "
                f"errors={total_errors} failed_leagues={len(failures)}"
            )
        )
        if failures:
            self.stdout.write(self.style.WARNING("Failed leagues:"))
            for f in failures:
                self.stdout.write(self.style.WARNING(f"  • {f}"))
