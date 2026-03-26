# League Endpoints

---

## Standings

```bash
# Primary — full standings data
curl "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"

# With season
curl "https://site.api.espn.com/apis/v2/sports/football/nfl/standings?season=2024"

# Core API standings
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/standings"
```

> ⚠️ `/apis/site/v2/sports/football/nfl/standings` — returns only a stub. Use `/apis/v2/` for full data.

**Response (trimmed):**
```json
{
  "uid": "s:20~l:28",
  "season": { "year": 2024, "type": 2 },
  "standings": {
    "entries": [
      {
        "team": { "id": "12", "displayName": "Kansas City Chiefs", "abbreviation": "KC" },
        "stats": [
          { "name": "wins", "displayValue": "15", "value": 15 },
          { "name": "losses", "displayValue": "2", "value": 2 },
          { "name": "winPercent", "displayValue": ".882", "value": 0.8824 },
          { "name": "divisionWins", "displayValue": "6", "value": 6 },
          { "name": "pointsFor", "displayValue": "371", "value": 371 },
          { "name": "pointsAgainst", "displayValue": "289", "value": 289 }
        ]
      }
    ]
  }
}
```

**Status:** VERIFIED ✅

---

## League-Wide Injury Report

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
      "team": { "id": "6", "abbreviation": "DAL", "displayName": "Dallas Cowboys" },
      "injuries": [
        {
          "athlete": {
            "id": "4241457",
            "fullName": "Micah Parsons",
            "position": { "abbreviation": "LB" },
            "jersey": "11"
          },
          "status": "Questionable",
          "type": { "description": "Ankle" },
          "date": "2025-01-02T05:00:00Z"
        }
      ]
    }
  ]
}
```

**Status:** VERIFIED ✅

---

## Transactions

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/transactions
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/transactions"
```

**Response (trimmed):**
```json
{
  "season": { "year": 2025, "type": 4 },
  "count": 458,
  "pageIndex": 1,
  "pageSize": 25,
  "transactions": [
    {
      "id": "001",
      "date": "2026-03-25T00:00:00Z",
      "description": "Re-signed OL Trent Williams",
      "team": { "id": "25", "abbreviation": "SF" },
      "type": "contract"
    }
  ]
}
```

**Status:** VERIFIED ✅

---

## News

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/news
```

| Param | Description |
|-------|-------------|
| `limit` | Number of articles (default 20) |

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/news?limit=20"
```

**Status:** VERIFIED ✅

---

## Calendar

```bash
# Full season calendar
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/calendar"

# Regular season weeks
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/calendar/regular-season"

# Postseason
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/calendar/postseason"

# Offseason
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/calendar/offseason"
```

**Status:** VERIFIED ✅

---

## Seasons

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons?limit=10"
```

**Status:** VERIFIED ✅

---

## Season Detail

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
  "abbreviation": "reg",
  "types": {
    "items": [
      { "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/1" },
      { "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2" },
      { "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/3" }
    ]
  }
}
```

**Status:** VERIFIED ✅

---

## Season Weeks

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/types/{type}/weeks
```

```bash
# All weeks in 2024 regular season
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/weeks?limit=20"
```

**Status:** VERIFIED ✅

---

## Conferences / Divisions

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/groups
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/groups"
```

**Status:** VERIFIED ✅

---

## Venues

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/venues
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/venues?limit=40"
```

**Status:** VERIFIED ✅

---

## QBR — Total Quarterback Rating

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/types/{type}/groups/{group}/qbr/{split}
```

| Param | Values |
|-------|--------|
| `type` | `1`=pre, `2`=reg, `3`=post |
| `group` | `1` (NFL) |
| `split` | `0`=totals, `1`=home, `2`=away |

```bash
# 2024 season QBR totals
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/groups/1/qbr/0"

# Week 18 QBR
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/weeks/18/qbr/0"
```

**Status:** VERIFIED ✅

---

## Draft

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/draft
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/draft"
```

**Status:** VERIFIED ✅

---

## Coaches

```bash
# All coaches for a season
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/coaches

# Individual coach
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/coaches/{coachId}
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/coaches?limit=32"
```

**Status:** PARTIALLY VERIFIED ✅

---

## Statistical Leaders

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/leaders
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/leaders"
```

**Status:** VERIFIED ✅

---

## Franchises

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/franchises
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/franchises?limit=32"
```

**Status:** VERIFIED ✅
