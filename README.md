# NFL Public API Documentation

**Disclaimer:** This documents NFL data APIs across multiple domains, including undocumented public endpoints used by NFL.com and ESPN's NFL data infrastructure. Not affiliated with the NFL or ESPN. Use responsibly.

---

## ☕ Support This Project

| Platform | Link |
|----------|------|
| ☕ Buy Me a Coffee | [buymeacoffee.com/pseudo_r](https://buymeacoffee.com/pseudo_r) |
| 💖 GitHub Sponsors | [github.com/sponsors/Kloverdevs](https://github.com/sponsors/Kloverdevs) |
| 💳 PayPal Donate | [PayPal (CAD)](https://www.paypal.com/donate/?business=H5VPFZ2EHVNBU&no_recurring=0&currency_code=CAD) |

---

## Table of Contents

- [Overview](#overview)
- [Base Domains](#base-domains)
- [Important: Authentication](#important-authentication)
- [Quick Start](#quick-start)
- [Game Endpoints](#game-endpoints)
- [Team Endpoints](#team-endpoints)
- [Player Endpoints](#player-endpoints)
- [League Endpoints](#league-endpoints)
- [Live / GameCenter Endpoints](#live--gamecenter-endpoints)
- [Additional Domains / Endpoint Families](#additional-domains--endpoint-families)
- [Endpoint Relationships](#endpoint-relationships)
- [Parameters Reference](#parameters-reference)
- [Notes / Quirks](#notes--quirks)
- [Docs](docs/)
- [CHANGELOG](CHANGELOG.md)

---

## Overview

NFL data is **not centralized in a single public API**. It is split across multiple domains:

- **`api.nfl.com`** — NFL's native API (requires OAuth bearer token, not publicly accessible)
- **`site.api.espn.com`** — ESPN's site-facing NFL data (scores, teams, rosters, injuries) — **fully public**
- **`sports.core.api.espn.com`** — ESPN's core API (deep stats, play-by-play, events, athletes) — **fully public**
- **`cdn.espn.com`** — CDN-optimized game packages (drives, plays, win probability) — **fully public**
- **`nextgenstats.nfl.com`** — NFL Next Gen Stats (requires NFL auth)
- **`feeds.nfl.com`** — Legacy NFL JSON feeds (restricted, 403 publicly)

### Why relies on ESPN instead of native NFL.com APIs?

Extensive web research and reverse-engineering of the NFL Mobile App and NFL.com reveals that **the NFL does not offer any public, unauthenticated JSON APIs.** 

- **Native Auth Lock:** All requests to `api.nfl.com` (both REST and the `/v3/shield` GraphQL endpoint) are strictly locked behind an OAuth 2.0 implementation. 
- **Reverse Engineering:** While developers have occasionally managed to extract `client_id` and `client_secret` pairs from local browser storage or by decompiling the NFL mobile app, these tokens rotate and are heavily monitored.
- **Legacy Feeds Deprecated:** Historically, domains like `static.nfl.com` and `feeds.nfl.com` offered public JSON (often used by tools like `nflscrapR`). These have been deprecated or locked behind 403 Forbidden walls.

Because of this fragmentation and strict security on official NFL properties, **the most complete, reliable, and publicly accessible NFL data is served through ESPN's public API infrastructure.**

**Authentication:** Most `espn.com` endpoints require no auth. All `api.nfl.com` endpoints require OAuth.

---

## Base Domains

| Domain | Auth Required | Purpose |
|--------|--------------|---------|
| `site.api.espn.com` | ❌ None | Scores, teams, rosters, news, injuries, transactions |
| `sports.core.api.espn.com` | ❌ None | Events, athletes, stats, play-by-play, odds, QBR |
| `cdn.espn.com` | ❌ None | CDN-optimized game packages |
| `site.web.api.espn.com` | ❌ None | Athlete profiles, stats, game logs |
| `api.nfl.com` | ✅ OAuth Bearer | NFL's native GraphQL + REST API |
| `nextgenstats.nfl.com` | ✅ NFL Auth | NFL Next Gen Stats (player tracking) |
| `feeds.nfl.com` | ✅ Restricted | Legacy NFL JSON feeds (403 publicly) |

---

## Important: Authentication

### Public Endpoints (ESPN-hosted NFL Data)

All `espn.com` domains are publicly accessible — no token needed.

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
```

### api.nfl.com (Requires OAuth)

NFL's native API requires a bearer token obtained via OAuth:

```bash
# Step 1: Get a bearer token
POST https://api.nfl.com/v1/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}
```

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

```bash
# Step 2: Use the token
curl -H "Authorization: Bearer {ACCESS_TOKEN}" \
  "https://api.nfl.com/v1/games?season=2024&seasonType=REG&week=1"
```

> ⚠️ Client credentials (`CLIENT_ID` / `CLIENT_SECRET`) are embedded in the NFL mobile app and browser clients. They can be extracted from network analysis but are not officially published.

---

## Quick Start

```bash
# NFL scoreboard (current week)
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

# NFL scoreboard (specific week + season)
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?week=1&seasontype=2&season=2024"

# NFL standings
curl "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"

# Dallas Cowboys roster
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/6/roster"

# NFL injury report (all teams)
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/injuries"

# Full game summary (boxscore + drives + plays)
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=401671827"

# Full game package (CDN — drives, plays, win probability, odds)
curl "https://cdn.espn.com/core/nfl/game?xhr=1&gameId=401671827"
```

---

## Game Endpoints

See full reference: [docs/game_endpoints.md](docs/game_endpoints.md)

### Scoreboard

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
```

| Param | Description | Example |
|-------|-------------|---------|
| `week` | NFL week number | `1`–`18` |
| `seasontype` | Season type | `1`=pre, `2`=reg, `3`=post |
| `season` | Year | `2024` |
| `dates` | Single date | `20241215` |

```bash
# Current week
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

# Week 1 of 2024 regular season
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?week=1&seasontype=2&season=2024"

# Specific date
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20241215"
```

**Response (trimmed):**
```json
{
  "leagues": [{ "id": "28", "name": "National Football League", "abbreviation": "NFL" }],
  "season": { "type": 2, "year": 2024 },
  "week": { "number": 1 },
  "events": [
    {
      "id": "401671731",
      "date": "2024-09-05T00:20:00Z",
      "name": "Green Bay Packers at Philadelphia Eagles",
      "shortName": "GB @ PHI",
      "season": { "year": 2024, "type": 2 },
      "competitions": [{
        "competitors": [
          { "id": "21", "team": { "abbreviation": "PHI" }, "score": "34", "homeAway": "home" },
          { "id": "9", "team": { "abbreviation": "GB" }, "score": "29", "homeAway": "away" }
        ],
        "status": { "type": { "name": "STATUS_FINAL", "completed": true } }
      }]
    }
  ]
}
```

**Status:** VERIFIED ✅

---

### Game Summary

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eventId}
```

Returns boxscore, drives, scoring plays, linescore, headlines, and game info in one payload.

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=401671827"
```

**Response (trimmed):**
```json
{
  "boxscore": {
    "teams": [
      {
        "team": { "id": "29", "abbreviation": "CAR", "displayName": "Carolina Panthers" },
        "statistics": [
          { "name": "firstDowns", "displayValue": "25", "label": "1st Downs" },
          { "name": "totalYards", "displayValue": "412", "label": "Total Yards" },
          { "name": "passingYards", "displayValue": "287", "label": "Passing Yards" }
        ]
      }
    ],
    "players": [{ "team": {}, "statistics": [{ "athletes": [] }] }]
  },
  "drives": { "current": {}, "previous": [] },
  "scoringPlays": [],
  "winprobability": [],
  "header": { "competitions": [{ "competitors": [], "status": {} }] }
}
```

**Status:** VERIFIED ✅

---

### CDN Game Package

```
GET https://cdn.espn.com/core/nfl/game?xhr=1&gameId={eventId}
```

Full game data package. Returns `gamepackageJSON` key containing drives, plays, boxscore, win probability, and odds.

```bash
# Full game package
curl "https://cdn.espn.com/core/nfl/game?xhr=1&gameId=401671827"

# Boxscore only
curl "https://cdn.espn.com/core/nfl/boxscore?xhr=1&gameId=401671827"

# Play-by-play only
curl "https://cdn.espn.com/core/nfl/playbyplay?xhr=1&gameId=401671827"

# Matchup / team comparison
curl "https://cdn.espn.com/core/nfl/matchup?xhr=1&gameId=401671827"
```

> Returns JSON when `?xhr=1` is passed. The key `gamepackageJSON` holds the full object.

**Status:** VERIFIED ✅

---

### Events (Core API)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events
```

| Param | Description | Example |
|-------|-------------|---------|
| `dates` | Filter by date | `20241215` |
| `week` | Week number | `1`–`18` |
| `season` | Season year | `2024` |
| `seasontype` | Season type | `2` |
| `limit` | Results per page | `16` |

```bash
# Events for Week 18, 2024 regular season
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/weeks/18/events?limit=16"

# All events by date
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events?dates=20241215&limit=20"
```

**Response (trimmed):**
```json
{
  "$meta": { "parameters": { "week": ["18"], "season": ["2024"], "seasontypes": ["2"] } },
  "count": 16,
  "pageIndex": 1,
  "pageSize": 16,
  "items": [
    { "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827" }
  ]
}
```

**Status:** VERIFIED ✅

---

### Single Event Detail (Core API)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827"
```

**Status:** VERIFIED ✅

---

### Play-by-Play (Core API)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}/competitions/{eventId}/plays
```

| Param | Description |
|-------|-------------|
| `limit` | Plays per page (max 300) |
| `page` | Page number |

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/plays?limit=100"
```

**Response (trimmed):**
```json
{
  "count": 168,
  "pageIndex": 1,
  "pageSize": 100,
  "items": [
    {
      "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/plays/4016718270001"
    }
  ]
}
```

**Status:** VERIFIED ✅

---

### Game Situation (Core API)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}/competitions/{eventId}/situation
```

Returns current game state: down, distance, yard line, possession, last play.

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/situation"
```

**Response (trimmed):**
```json
{
  "lastPlay": { "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/plays/4016718274717" },
  "down": 4,
  "yardLine": 34,
  "distance": 10,
  "possession": { "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/competitors/29" }
}
```

**Status:** VERIFIED ✅

---

### Win Probabilities

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}/competitions/{eventId}/probabilities
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/probabilities?limit=20"
```

**Status:** VERIFIED ✅

---

### Odds

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}/competitions/{eventId}/odds
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/odds"
```

**Status:** VERIFIED ✅

---

## Team Endpoints

See full reference: [docs/team_endpoints.md](docs/team_endpoints.md)

### All Teams

```bash
# Site API — user-friendly
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"

# Core API — richer object graph
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams?limit=32"
```

**Status:** VERIFIED ✅

---

### Team Detail

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}
```

| NFL Team | ESPN ID |
|----------|---------|
| Arizona Cardinals | 22 |
| Atlanta Falcons | 1 |
| Baltimore Ravens | 33 |
| Buffalo Bills | 2 |
| Carolina Panthers | 29 |
| Chicago Bears | 3 |
| Cincinnati Bengals | 4 |
| Cleveland Browns | 5 |
| Dallas Cowboys | 6 |
| Denver Broncos | 7 |
| Detroit Lions | 8 |
| Green Bay Packers | 9 |
| Houston Texans | 34 |
| Indianapolis Colts | 11 |
| Jacksonville Jaguars | 30 |
| Kansas City Chiefs | 12 |
| Las Vegas Raiders | 13 |
| Los Angeles Chargers | 24 |
| Los Angeles Rams | 14 |
| Miami Dolphins | 15 |
| Minnesota Vikings | 16 |
| New England Patriots | 17 |
| New Orleans Saints | 18 |
| New York Giants | 19 |
| New York Jets | 20 |
| Philadelphia Eagles | 21 |
| Pittsburgh Steelers | 23 |
| San Francisco 49ers | 25 |
| Seattle Seahawks | 26 |
| Tampa Bay Buccaneers | 27 |
| Tennessee Titans | 10 |
| Washington Commanders | 28 |

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/12"
```

**Response (trimmed):**
```json
{
  "team": {
    "id": "12",
    "uid": "s:20~l:28~t:12",
    "slug": "kansas-city-chiefs",
    "abbreviation": "KC",
    "displayName": "Kansas City Chiefs",
    "shortDisplayName": "Chiefs",
    "color": "e31837",
    "alternateColor": "ffb81c",
    "logos": [{ "href": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png" }],
    "venue": { "id": "3636", "fullName": "GEHA Field at Arrowhead Stadium", "city": "Kansas City" }
  }
}
```

**Status:** VERIFIED ✅

---

### Team Roster

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}/roster
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/6/roster"
```

**Response (trimmed):**
```json
{
  "season": { "year": 2025, "type": 4 },
  "athletes": [
    {
      "position": "Quarterback",
      "items": [
        {
          "id": "3054211",
          "fullName": "Dak Prescott",
          "displayName": "Dak Prescott",
          "jersey": "4",
          "position": { "abbreviation": "QB" }
        }
      ]
    }
  ]
}
```

**Status:** VERIFIED ✅

---

### Team Schedule

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}/schedule
```

| Param | Description |
|-------|-------------|
| `season` | Year (e.g. `2024`) |
| `seasontype` | `1`=pre, `2`=reg, `3`=post |

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/6/schedule?season=2024"
```

**Status:** VERIFIED ✅

---

### Team Depth Chart

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}/depthcharts
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/6/depthcharts"
```

**Status:** VERIFIED ✅

---

### Team Injuries

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}/injuries
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/6/injuries"
```

**Status:** VERIFIED ✅

---

### Team Statistical Leaders

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}/leaders
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/6/leaders"
```

**Status:** VERIFIED ✅

---

### Season-Specific Teams (Core API)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/teams
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/teams?limit=32"
```

**Status:** VERIFIED ✅

---

## Player Endpoints

See full reference: [docs/player_endpoints.md](docs/player_endpoints.md)

### Player Profile (Site API)

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/athletes/{athleteId}
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/athletes/3054211"
```

**Status:** VERIFIED ✅

---

### Player Profile (Core API — season-scoped)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/athletes/{athleteId}
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/athletes/3054211"
```

**Response (trimmed):**
```json
{
  "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/athletes/3054211",
  "id": "3054211",
  "firstName": "Dak",
  "lastName": "Prescott",
  "fullName": "Dak Prescott",
  "displayName": "Dak Prescott",
  "jersey": "4",
  "position": { "abbreviation": "QB", "name": "Quarterback" },
  "team": { "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams/6" }
}
```

**Status:** VERIFIED ✅

---

### Season-Scoped Player Statistics

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/athletes/{athleteId}/statistics
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/athletes/3054211/statistics"
```

**Status:** VERIFIED ✅

---

### Player Stats Log (Game-by-Game)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{athleteId}/statisticslog
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/3054211/statisticslog"
```

**Status:** VERIFIED ✅

---

### Player Event Log

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{athleteId}/eventlog
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/3054211/eventlog"
```

**Status:** VERIFIED ✅

---

### All Active Athletes (Core API)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes
```

| Param | Description |
|-------|-------------|
| `active` | `true` for active only |
| `limit` | Results per page |
| `page` | Page number |
| `position` | Filter by position slug |

```bash
# All active players
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes?active=true&limit=100"
```

**Status:** VERIFIED ✅

---

### Season Athletes (Core API)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/athletes
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/athletes?limit=100"
```

**Status:** VERIFIED ✅

---

### Player News

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/athletes/{athleteId}/news
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/athletes/3054211/news"
```

**Status:** VERIFIED ✅

---

## League Endpoints

See full reference: [docs/league_endpoints.md](docs/league_endpoints.md)

### Standings

```bash
# Primary (full data)
curl "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"

# Season-specific
curl "https://site.api.espn.com/apis/v2/sports/football/nfl/standings?season=2024"

# Core API standings
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/standings"
```

> ⚠️ `/apis/site/v2/sports/football/nfl/standings` returns a stub only. Use `/apis/v2/` instead.

**Status:** VERIFIED ✅

---

### League-Wide Injury Report

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/injuries
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/injuries"
```

**Response (trimmed):**
```json
{
  "season": { "year": 2025, "type": 4 },
  "injuries": [
    {
      "team": { "id": "6", "abbreviation": "DAL" },
      "injuries": [
        {
          "athlete": { "fullName": "Micah Parsons", "position": { "abbreviation": "LB" } },
          "status": "Questionable",
          "type": { "description": "Ankle" }
        }
      ]
    }
  ]
}
```

**Status:** VERIFIED ✅

---

### Transactions

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/transactions
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/transactions"
```

**Response (trimmed):**
```json
{
  "count": 458,
  "transactions": [
    {
      "date": "2026-03-25T00:00:00Z",
      "description": "Re-signed OL Trent Williams",
      "team": { "abbreviation": "SF" },
      "type": "contract"
    }
  ]
}
```

**Status:** VERIFIED ✅

---

### News

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/news
```

| Param | Description |
|-------|-------------|
| `limit` | Number of articles |

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/news?limit=20"
```

**Status:** VERIFIED ✅

---

### Season Calendar

```bash
# Full calendar (all weeks and dates)
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/calendar"

# Regular season only
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/calendar/regular-season"

# Postseason
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/calendar/postseason"

# Offseason
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/calendar/offseason"
```

**Status:** VERIFIED ✅

---

### Seasons

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons?limit=10"
```

**Status:** VERIFIED ✅

---

### Season Detail

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024"
```

**Response (trimmed):**
```json
{
  "id": "2024",
  "year": 2024,
  "startDate": "2024-07-30T07:00:00Z",
  "endDate": "2025-02-10T07:59:00Z",
  "displayName": "2024",
  "name": "Regular Season",
  "abbreviation": "reg"
}
```

**Status:** VERIFIED ✅

---

### QBR (Total Quarterback Rating)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/types/{type}/groups/{group}/qbr/{split}
```

| Param | Values |
|-------|--------|
| `type` | `1`=pre, `2`=reg, `3`=post |
| `group` | `1`=NFL |
| `split` | `0`=totals, `1`=home, `2`=away |

```bash
# 2024 Season QBR totals
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/groups/1/qbr/0"

# Weekly QBR
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/weeks/18/qbr/0"
```

**Status:** VERIFIED ✅

---

### Draft

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/draft
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/draft"
```

**Status:** VERIFIED ✅

---

### Venues

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/venues
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/venues?limit=32"
```

**Status:** VERIFIED ✅

---

### Groups (Conferences / Divisions)

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/groups
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/groups"
```

**Status:** VERIFIED ✅

---

## Live / GameCenter Endpoints

NFL.com's GameCenter previously exposed JSON feeds at `/liveupdate/game-center/{gameId}/{gameId}_gtd.json` — this endpoint is **no longer publicly accessible** (returns 404).

ESPN's CDN endpoints are the modern equivalent, updated during live games:

```bash
# Full live game package (updates during game)
curl "https://cdn.espn.com/core/nfl/game?xhr=1&gameId={eventId}"

# Live scoreboard
curl "https://cdn.espn.com/core/nfl/scoreboard?xhr=1"

# Live play-by-play
curl "https://cdn.espn.com/core/nfl/playbyplay?xhr=1&gameId={eventId}"

# Live boxscore
curl "https://cdn.espn.com/core/nfl/boxscore?xhr=1&gameId={eventId}"

# Live game situation (down/distance/possession)
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}/competitions/{eventId}/situation"
```

**Status:** VERIFIED ✅

---

### api.nfl.com (Authenticated)

When a valid bearer token is available, the NFL's native API exposes these endpoints:

```bash
# Games by week
GET https://api.nfl.com/v1/games?season={year}&seasonType={REG|PRE|POST}&week={n}

# Single game
GET https://api.nfl.com/v1/games/{gameId}

# Standings
GET https://api.nfl.com/v1/standings?season={year}&seasonType={REG}

# Teams
GET https://api.nfl.com/v1/teams

# Single team
GET https://api.nfl.com/v1/teams/{teamId}

# Team roster
GET https://api.nfl.com/v1/teams/{teamId}/roster

# Players
GET https://api.nfl.com/v1/players

# Player profile
GET https://api.nfl.com/v1/players/{playerId}
```

All require `Authorization: Bearer {token}` header.

**Status:** UNVERIFIED (auth required)

---

### Next Gen Stats API (Authenticated)

```bash
# Passing stats
GET https://nextgenstats.nfl.com/api/statboard/passing?season={year}&seasonType={REG|PRE|POST}

# Rushing stats
GET https://nextgenstats.nfl.com/api/statboard/rushing?season={year}&seasonType={REG|PRE|POST}

# Receiving stats
GET https://nextgenstats.nfl.com/api/statboard/receiving?season={year}&seasonType={REG|PRE|POST}
```

Requires NFL authentication (session cookie from nextgenstats.nfl.com login).

**Status:** UNVERIFIED (auth required)

---

## Additional Domains / Endpoint Families

### `site.api.espn.com` — Site-Facing NFL Data

The primary public NFL data API. Powers ESPN.com's NFL pages.

**Base pattern:**
```
https://site.api.espn.com/apis/site/v2/sports/football/nfl/{resource}
```

| Resource | Description |
|----------|-------------|
| `scoreboard` | Live scores + scheduled games |
| `teams` | All 32 teams |
| `teams/{id}` | Single team |
| `teams/{id}/roster` | Team roster |
| `teams/{id}/schedule` | Team schedule |
| `teams/{id}/depthcharts` | Depth chart by position |
| `teams/{id}/injuries` | Team injury report |
| `teams/{id}/leaders` | Team statistical leaders |
| `teams/{id}/news` | Team news |
| `teams/{id}/record` | Win/loss record |
| `injuries` | League-wide injury report (all teams) |
| `transactions` | Signings, trades, free agent moves |
| `news` | NFL news feed |
| `calendar` | Season calendar with all weeks |
| `calendar/regular-season` | Regular season weeks |
| `calendar/postseason` | Playoff dates |
| `calendar/offseason` | Offseason dates |
| `groups` | Conferences + divisions |
| `summary?event={id}` | Full game summary (boxscore, drives, scoring) |
| `athletes/{id}` | Player profile |
| `athletes/{id}/news` | Player news |

---

### `sports.core.api.espn.com` — Core NFL Data

Deep data API. Returns `$ref` links that resolve to full objects.

**Base pattern:**
```
https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/{resource}
```

| Resource | Description |
|----------|-------------|
| `events` | Game events (paginated) |
| `events/{id}` | Single event detail |
| `events/{id}/competitions/{id}/plays` | Play-by-play |
| `events/{id}/competitions/{id}/situation` | Down/distance/possession |
| `events/{id}/competitions/{id}/odds` | Game odds |
| `events/{id}/competitions/{id}/probabilities` | Win probabilities |
| `events/{id}/competitions/{id}/broadcasts` | TV broadcast info |
| `athletes` | All athletes (paginated) |
| `athletes/{id}` | Single athlete |
| `athletes/{id}/statisticslog` | Game-by-game log |
| `athletes/{id}/eventlog` | Event participation history |
| `seasons` | Season list |
| `seasons/{year}` | Season detail |
| `seasons/{year}/teams` | Teams in season |
| `seasons/{year}/athletes` | Athletes in season |
| `seasons/{year}/athletes/{id}` | Season-scoped athlete |
| `seasons/{year}/athletes/{id}/statistics` | Season statistics |
| `seasons/{year}/draft` | Draft info |
| `seasons/{year}/types/2/groups/1/qbr/0` | QBR totals |
| `seasons/{year}/types/2/weeks/{n}/qbr/0` | Weekly QBR |
| `standings` | League standings |
| `teams` | Teams |
| `venues` | Stadiums |
| `franchises` | Franchise history |

---

### `cdn.espn.com` — CDN Game Packages

Optimized for fast delivery during live games. Requires `?xhr=1`.

```
https://cdn.espn.com/core/nfl/{resource}?xhr=1
```

| Resource | Description |
|----------|-------------|
| `scoreboard` | Live scoreboard |
| `game?gameId={id}` | Full game package (drives, plays, probability) |
| `boxscore?gameId={id}` | Boxscore |
| `playbyplay?gameId={id}` | Play-by-play |
| `matchup?gameId={id}` | Team comparison / matchup |

---

### `api.nfl.com` — NFL Native API (Auth Required)

NFL's own API. GraphQL shield at `/v3/shield/` and REST at `/v1/`.

```
https://api.nfl.com/v1/{resource}
```

> All endpoints require `Authorization: Bearer {token}`. Token obtained via:
> `POST https://api.nfl.com/v1/oauth/token` with `client_credentials` flow.

---

### `nextgenstats.nfl.com` — NFL Next Gen Stats (Auth Required)

Player tracking data powered by AWS. Requires NFL session auth.

```
https://nextgenstats.nfl.com/api/statboard/{category}?season={year}&seasonType={type}
```

Categories: `passing`, `rushing`, `receiving`

---

### `feeds.nfl.com` — Legacy NFL Feeds (Restricted)

Legacy JSON feed system. Returns 403 publicly.

```
https://feeds.nfl.com/feeds-rs/standings/{year}.json
https://feeds.nfl.com/feeds-rs/scores/{year}/{type}/{week}.json
```

---

## Endpoint Relationships

```
schedule/scoreboard
    └── event.id (eventId)
            ├── /summary?event={id}          → boxscore, drives, scoring plays
            ├── cdn.espn.com/core/nfl/game?gameId={id}  → full CDN package
            ├── /events/{id}/competitions/{id}/plays      → play-by-play
            ├── /events/{id}/competitions/{id}/situation  → live game state
            ├── /events/{id}/competitions/{id}/odds       → betting odds
            └── /events/{id}/competitions/{id}/probabilities → win probability

teams
    └── team.id (teamId)
            ├── /teams/{id}/roster           → players → athleteId
            ├── /teams/{id}/schedule         → games → eventId
            ├── /teams/{id}/depthcharts      → position groups
            └── /teams/{id}/injuries         → injury statuses

athletes
    └── athlete.id (athleteId)
            ├── /athletes/{id}               → profile
            ├── /seasons/{year}/athletes/{id}/statistics  → season stats
            ├── /athletes/{id}/statisticslog             → game-by-game
            └── /athletes/{id}/eventlog                  → event history
```

---

## Parameters Reference

| Param | Description | Example |
|-------|-------------|---------|
| `week` | NFL week number | `1`–`18` |
| `season` | Season year | `2024` |
| `seasontype` | Season type | `1`=pre, `2`=reg, `3`=post |
| `dates` | Filter by date (YYYYMMDD) | `20241215` |
| `limit` | Results per page | `100` |
| `page` | Pagination | `1` |
| `active` | Active player filter | `true` / `false` |
| `xhr` | CDN JSON signal | `1` |

### Season Types

| Type | Value |
|------|-------|
| Preseason | `1` |
| Regular Season | `2` |
| Postseason | `3` |
| Offseason | `4` |

### NFL Team IDs (ESPN)

See the full table in [Team Endpoints](#team-detail) above.

---

## Notes / Quirks

- **`/apis/site/v2/` standings** returns a stub — always use `/apis/v2/sports/football/nfl/standings`
- **`eventId` = `competitionId`** in `sports.core.api.espn.com` — they are the same value
- **CDN endpoints** require `?xhr=1` to return JSON; without it, they return HTML
- **`$ref` links** in Core API responses are fully resolvable URLs — follow them for nested detail
- **GameCenter legacy URL** (`nfl.com/liveupdate/game-center/...`) no longer works (404)
- **`api.nfl.com`** uses the same game IDs as ESPN (e.g. `2024123000` format: `{YYYYMMDD}{homeTeamId}`)
- **NFL season year** refers to the year the season starts, not the Super Bowl year
- **Page size** on Core API defaults vary; pass `limit=100` or higher for large datasets
- **`dates` range** on site API: `20241201-20241231` returns all games in December

---

## Contributing

Found a new endpoint? Open an issue or PR!

## License

MIT License

---

*Last Updated: March 2026 · Domains: site.api.espn.com · sports.core.api.espn.com · cdn.espn.com · api.nfl.com (auth) · nextgenstats.nfl.com (auth) · feeds.nfl.com (restricted)*
