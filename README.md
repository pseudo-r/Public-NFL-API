# Public NFL API Documentation

An unofficial, endpoint-first documentation repository for the native `api.nfl.com` JSON APIs used by NFL.com and the official NFL mobile apps.

> **⚠️ WARNING: STRICTLY AUTHENTICATED**
> Unlike other sports data APIs, the native NFL data APIs do **not** offer any unauthenticated endpoints. Every single request requires an active OAuth 2.0 Bearer token.

---

## Objective

To provide a clean, copy-pasteable reference for the official NFL.com REST APIs to retrieve game, team, player, and statistical data.

---

## Authentication (OAuth 2.0)

Every request to `api.nfl.com` (both REST and the `/v3/shield` GraphQL endpoint) is locked behind a stringent OAuth 2.0 implementation. 

### Generating a Token

You must negotiate a `client_credentials` grant with the NFL identity server. 

```bash
POST https://api.nfl.com/identity/v1/token/client
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id={YOUR_CLIENT_ID}&client_secret={YOUR_CLIENT_SECRET}
```

**Where to get credentials:**
The NFL **does not** issue public API keys. Developers seeking to use these endpoints must either:
1. Decompile the official NFL mobile application to extract hardcoded or rotating client secrets.
2. Inspect browser storage (`localStorage`) on `nfl.com` stats pages to extract temporary `clientId` and browser `clientSecret` pairs.

*Note: The NFL actively monitors and rotates these secrets to prevent unauthorized data extraction.*

### Using the Token

Any request to the endpoints documented in this repository must include the generated token in the Authorization header.

```bash
curl "https://api.nfl.com/v1/games?season=2024&seasonType=REG&week=1" \
  -H "Authorization: Bearer <your_token_here>"
```

---

## Base Domains

All operations in this documentation use the following base domains:

| Domain | Description |
|--------|-------------|
| `api.nfl.com` | Primary REST and GraphQL API. Requires Bearer Auth. |
| `nextgenstats.nfl.com` | AWS-powered Next Gen Stats. Requires NFL.com session. |

---

## Endpoints

Documentation is split by domain. Note that all endpoints return `401 Unauthorized` if hit without valid credentials.

* [Game Endpoints](docs/game_endpoints.md) — Scoreboard, game logs, play-by-play
* [Team Endpoints](docs/team_endpoints.md) — Rosters, schedules, team stats
* [Player Endpoints](docs/player_endpoints.md) — Profiles, season stats
* [League Endpoints](docs/league_endpoints.md) — Standings, draft data

---

## Philosophy

Following the style of the ESPN Public API project:
* **Endpoint-first:** URLs and HTTP methods are the primary focus.
* **Minimal explanation:** The endpoints describe themselves.
* **Real requests:** Curl examples provided (requiring you to substitute your Bearer token).

## Contributing

Found a new OAuth workaround or a new endpoint? Open a PR following the format in `CONTRIBUTING.md`.
