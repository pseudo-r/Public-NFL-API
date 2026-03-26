# Additional Domains / Endpoint Families

A comprehensive map of all NFL data API domains and feed systems.

---

## `site.api.espn.com` — Primary Public NFL API

**Status:** VERIFIED ✅ — No auth required  
**Purpose:** Scores, teams, rosters, news, injuries, transactions  

```
https://site.api.espn.com/apis/site/v2/sports/football/nfl/{resource}
```

Powers ESPN.com NFL pages. Best entry point for most NFL data needs.

Example endpoints:
```bash
https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams
https://site.api.espn.com/apis/site/v2/sports/football/nfl/injuries
https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=401671827
```

---

## `sports.core.api.espn.com` — Core NFL Data

**Status:** VERIFIED ✅ — No auth required  
**Purpose:** Events, athletes, stats, play-by-play, odds, probabilities, QBR  

```
https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/{resource}
```

Returns `$ref` linked objects. Follow `$ref` URLs to resolve nested data.

Example endpoints:
```bash
https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events
https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{id}/competitions/{id}/plays
https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/athletes?limit=100
https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/groups/1/qbr/0
```

---

## `cdn.espn.com` — CDN Game Packages

**Status:** VERIFIED ✅ — No auth required  
**Purpose:** Optimized live game data (drives, plays, win probability, odds)  

```
https://cdn.espn.com/core/nfl/{resource}?xhr=1
```

- Requires `?xhr=1` to return JSON
- Updated in real-time during live games
- `gamepackageJSON` key contains the full nested payload

Example endpoints:
```bash
https://cdn.espn.com/core/nfl/scoreboard?xhr=1
https://cdn.espn.com/core/nfl/game?xhr=1&gameId=401671827
https://cdn.espn.com/core/nfl/boxscore?xhr=1&gameId=401671827
https://cdn.espn.com/core/nfl/playbyplay?xhr=1&gameId=401671827
https://cdn.espn.com/core/nfl/matchup?xhr=1&gameId=401671827
```

---

## `api.nfl.com` — NFL Native API (Auth Required)

**Status:** UNVERIFIED (OAuth required)  
**Purpose:** NFL's own REST + GraphQL API  

```
https://api.nfl.com/v1/{resource}
https://api.nfl.com/v3/shield/  (GraphQL)
```

Requires OAuth 2.0 bearer token (`client_credentials` flow).

```bash
# Auth
POST https://api.nfl.com/v1/oauth/token
Content-Type: application/x-www-form-urlencoded
Body: grant_type=client_credentials&client_id={id}&client_secret={secret}
```

Known REST endpoints:
```bash
GET https://api.nfl.com/v1/teams
GET https://api.nfl.com/v1/teams/{teamId}
GET https://api.nfl.com/v1/teams/{teamId}/roster
GET https://api.nfl.com/v1/games?season={year}&seasonType={type}&week={n}
GET https://api.nfl.com/v1/games/{gameId}
GET https://api.nfl.com/v1/standings?season={year}&seasonType={type}
GET https://api.nfl.com/v1/players
GET https://api.nfl.com/v1/players/{playerId}
```

GraphQL schema (shield endpoint):
```bash
POST https://api.nfl.com/v3/shield/
Content-Type: application/json
Body: { "query": "{ viewer { ... } }" }
```

> Client credentials are embedded in NFL.com and the NFL mobile app. They are not officially published.

---

## `nextgenstats.nfl.com` — NFL Next Gen Stats (Auth Required)

**Status:** UNVERIFIED (NFL session required)  
**Purpose:** AWS-powered player tracking data  

```
https://nextgenstats.nfl.com/api/statboard/{category}
```

| Param | Values |
|-------|--------|
| `season` | Year (e.g. `2024`) |
| `seasonType` | `REG`, `PRE`, `POST` |
| `week` | Week number |

Known endpoint categories:
```bash
https://nextgenstats.nfl.com/api/statboard/passing?season=2024&seasonType=REG
https://nextgenstats.nfl.com/api/statboard/rushing?season=2024&seasonType=REG
https://nextgenstats.nfl.com/api/statboard/receiving?season=2024&seasonType=REG
```

Returns player tracking metrics: speed, acceleration, separation, air yards, completion probability, etc.

> Requires NFL.com session cookie obtained after login.

---

## `feeds.nfl.com` — Legacy NFL Feeds (Restricted)

**Status:** Restricted (403 publicly)  
**Purpose:** Legacy JSON data feed system  

```
https://feeds.nfl.com/feeds-rs/standings/{year}.json
https://feeds.nfl.com/feeds-rs/scores/{year}/{type}/{week}.json
```

Historically these feeds were publicly accessible. Now return 403 without proper auth headers.

---

## `site.web.api.espn.com` — ESPN Web API

**Status:** PARTIALLY VERIFIED  
**Purpose:** Athlete profiling, stats, game logs  

```
https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{id}/{resource}
```

> Note: Some endpoints return 404 for NFL (works reliably for NBA/MLB). Test before relying on.

Known working:
```bash
# Statistics leaderboard
https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?season=2024&seasontype=2&category=0
```

---

## Relationship Between Domains

```
api.nfl.com           → NFL-native game IDs (format: {YYYYMMDD}{homeTeamId})
                             ↕
ESPN game IDs (eventId)  → used in all espn.com domains
```

Both systems track the same games but IDs differ. ESPN's `eventId` (e.g. `401671827`) 
is the most widely supported ID across all public endpoints.

NFL.com game ID format: `{YYYYMMDD}{homeTeam3DigitId}` (e.g. `2024010500027`)
