# Game Endpoints

All endpoints on this page return NFL game data. Most are publicly accessible without authentication.

---

## Scoreboard

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
```

| Param | Description | Example |
|-------|-------------|---------|
| `week` | NFL week | `1`–`18` |
| `seasontype` | `1`=pre, `2`=reg, `3`=post | `2` |
| `season` | Year | `2024` |
| `dates` | Single date | `20241215` |

```bash
# Current week
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

# Week 18, 2024 regular season
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?week=18&seasontype=2&season=2024"

# All games on a date
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20241215"
```

**Response (trimmed):**
```json
{
  "leagues": [{ "id": "28", "name": "National Football League", "abbreviation": "NFL" }],
  "season": { "type": 2, "year": 2024 },
  "week": { "number": 18 },
  "events": [
    {
      "id": "401671827",
      "date": "2025-01-05T18:00:00Z",
      "name": "Carolina Panthers at Tampa Bay Buccaneers",
      "shortName": "CAR @ TB",
      "season": { "year": 2024, "type": 2 },
      "week": { "number": 18 },
      "competitions": [
        {
          "id": "401671827",
          "competitors": [
            { "id": "27", "homeAway": "home", "score": "48", "team": { "abbreviation": "TB" }, "winner": true },
            { "id": "29", "homeAway": "away", "score": "30", "team": { "abbreviation": "CAR" }, "winner": false }
          ],
          "venue": { "fullName": "Raymond James Stadium", "city": "Tampa", "state": "FL" },
          "status": { "type": { "name": "STATUS_FINAL", "completed": true }, "displayClock": "0:00", "period": 4 }
        }
      ]
    }
  ]
}
```

**Status:** VERIFIED ✅

---

## Game Summary

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={eventId}
```

One-stop endpoint: boxscore + drives + scoring plays + linescore + game info.

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=401671827"
```

**Response (trimmed):**
```json
{
  "boxscore": {
    "teams": [
      {
        "team": { "id": "27", "abbreviation": "TB", "displayName": "Tampa Bay Buccaneers" },
        "statistics": [
          { "name": "firstDowns", "displayValue": "25", "label": "1st Downs" },
          { "name": "totalYards", "displayValue": "412", "label": "Total Yards" },
          { "name": "passingYards", "displayValue": "287", "label": "Passing Yards" },
          { "name": "rushingYards", "displayValue": "125", "label": "Rushing Yards" },
          { "name": "turnovers", "displayValue": "1", "label": "Turnovers" }
        ]
      }
    ],
    "players": [
      {
        "team": { "id": "27" },
        "statistics": [
          {
            "name": "passingYards",
            "athletes": [
              {
                "athlete": { "id": "3915511", "fullName": "Baker Mayfield" },
                "stats": ["328", "25/37", "2", "0", "113.4"]
              }
            ]
          }
        ]
      }
    ]
  },
  "drives": {
    "previous": [
      {
        "id": "4016718270001",
        "description": "Touchdown",
        "team": { "abbreviation": "TB" },
        "start": { "period": 1, "clock": "14:52", "yardLine": 25 },
        "end": { "period": 1, "clock": "11:30", "yardLine": 0 },
        "yards": 75,
        "plays": 8,
        "result": "TD"
      }
    ]
  },
  "scoringPlays": [
    {
      "id": "4016718270152",
      "type": { "id": "6", "text": "Rushing Touchdown" },
      "period": { "number": 1 },
      "clock": { "displayValue": "11:30" },
      "team": { "id": "27" },
      "awayScore": 0,
      "homeScore": 7,
      "text": "Rachaad White 12 yard rush"
    }
  ],
  "winprobability": [
    {
      "sequenceNumber": "1",
      "homeWinPercentage": 0.6234,
      "tiePercentage": 0.0,
      "secondsLeft": 3600
    }
  ]
}
```

**Status:** VERIFIED ✅

---

## CDN Game Package

```
GET https://cdn.espn.com/core/nfl/game?xhr=1&gameId={eventId}
```

Full game data package. All `gamepackageJSON` nested keys are present.

```bash
# Full package
curl "https://cdn.espn.com/core/nfl/game?xhr=1&gameId=401671827"

# Boxscore only
curl "https://cdn.espn.com/core/nfl/boxscore?xhr=1&gameId=401671827"

# Play-by-play only
curl "https://cdn.espn.com/core/nfl/playbyplay?xhr=1&gameId=401671827"

# Matchup view
curl "https://cdn.espn.com/core/nfl/matchup?xhr=1&gameId=401671827"
```

**Notes:**
- Requires `?xhr=1` to get JSON (without it returns HTML)
- `gamepackageJSON` key contains the full nested payload
- Updated in real-time during live games

**Status:** VERIFIED ✅

---

## Events (Core API)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events
```

Returns a paginated list of `$ref` links to event objects.

```bash
# Events by date
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events?dates=20241215"

# Week-specific events (recommended)
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/weeks/18/events?limit=16"
```

**Response (trimmed):**
```json
{
  "$meta": { "parameters": { "week": ["18"], "season": ["2024"], "seasontypes": ["2"] } },
  "count": 16,
  "pageIndex": 1,
  "pageSize": 16,
  "pageCount": 1,
  "items": [
    { "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827?lang=en&region=us" },
    { "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671828?lang=en&region=us" }
  ]
}
```

**Status:** VERIFIED ✅

---

## Single Event (Core API)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827"
```

**Status:** VERIFIED ✅

---

## Play-by-Play

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}/competitions/{eventId}/plays
```

> `eventId` and `competitionId` are identical for NFL games.

| Param | Description |
|-------|-------------|
| `limit` | Plays per page (max ~300) |
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
  "pageCount": 2,
  "items": [
    { "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/plays/4016718270001?lang=en&region=us" }
  ]
}
```

**Status:** VERIFIED ✅

---

## Game Situation (Live State)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}/competitions/{eventId}/situation
```

Returns current down, distance, yard line, and possession. Only meaningful during live games.

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/situation"
```

**Response (trimmed):**
```json
{
  "lastPlay": { "$ref": "...plays/4016718274717" },
  "down": 4,
  "yardLine": 34,
  "distance": 10,
  "isRedZone": false,
  "homeTimeouts": 1,
  "awayTimeouts": 2,
  "possession": { "$ref": "...competitors/29" }
}
```

**Status:** VERIFIED ✅

---

## Win Probabilities

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}/competitions/{eventId}/probabilities
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/probabilities?limit=50"
```

**Response (trimmed):**
```json
{
  "count": 168,
  "items": [
    {
      "sequenceNumber": "1",
      "homeWinPercentage": 0.5512,
      "awayWinPercentage": 0.4488,
      "tiePercentage": 0.0,
      "play": { "$ref": "...plays/4016718270001" },
      "lastModified": "2025-01-05T23:04:52Z"
    }
  ]
}
```

**Status:** VERIFIED ✅

---

## Odds

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}/competitions/{eventId}/odds
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/odds"
```

**Response (trimmed):**
```json
{
  "count": 5,
  "items": [
    {
      "provider": { "id": "41", "name": "DraftKings", "priority": 1 },
      "details": "TB -9.5",
      "overUnder": 43.5,
      "spread": -9.5,
      "homeTeamOdds": { "favorite": true, "moneyLine": -400, "spreadOdds": -115 },
      "awayTeamOdds": { "favorite": false, "moneyLine": 320, "spreadOdds": -105 }
    }
  ]
}
```

**Betting Provider IDs:**

| Provider | ID |
|----------|-----|
| Caesars | 38 |
| FanDuel | 37 |
| DraftKings | 41 |
| BetMGM | 58 |
| ESPN BET | 68 |

**Status:** VERIFIED ✅

---

## Broadcasts

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}/competitions/{eventId}/broadcasts
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/broadcasts"
```

**Status:** VERIFIED ✅

---

## Officials

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{eventId}/competitions/{eventId}/officials
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671827/competitions/401671827/officials"
```

**Status:** VERIFIED ✅
