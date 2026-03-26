# Player Endpoints

---

## Player Profile (Site API)

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/athletes/{athleteId}
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/athletes/3054211"
```

**Status:** VERIFIED ✅

---

## Season-Scoped Player (Core API)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/athletes/{athleteId}
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/athletes/3054211"
```

**Response (trimmed):**
```json
{
  "id": "3054211",
  "firstName": "Dak",
  "lastName": "Prescott",
  "fullName": "Dak Prescott",
  "displayName": "Dak Prescott",
  "shortName": "D. Prescott",
  "weight": 238,
  "displayWeight": "238 lbs",
  "height": 74,
  "displayHeight": "6'2\"",
  "age": 31,
  "dateOfBirth": "1993-07-29T07:00:00Z",
  "birthPlace": { "city": "Sulphur", "state": "Louisiana", "country": "USA" },
  "jersey": "4",
  "slug": "dak-prescott",
  "position": { "id": "11", "name": "Quarterback", "abbreviation": "QB" },
  "experience": { "years": 9 },
  "college": { "id": "249", "name": "Mississippi State", "abbreviation": "MSST" },
  "team": { "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams/6" }
}
```

**Status:** VERIFIED ✅

---

## Season Statistics

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/athletes/{athleteId}/statistics
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/athletes/3054211/statistics"
```

**Response (trimmed):**
```json
{
  "splits": {
    "categories": [
      {
        "name": "passing",
        "displayName": "Passing",
        "stats": [
          { "name": "completions", "displayValue": "397", "value": 397 },
          { "name": "passingAttempts", "displayValue": "590", "value": 590 },
          { "name": "passingYards", "displayValue": "4516", "value": 4516 },
          { "name": "touchdowns", "displayValue": "34", "value": 34 },
          { "name": "interceptions", "displayValue": "9", "value": 9 },
          { "name": "QBRating", "displayValue": "105.2", "value": 105.2 }
        ]
      }
    ]
  }
}
```

**Status:** VERIFIED ✅

---

## Game-by-Game Stats Log

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{athleteId}/statisticslog
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/3054211/statisticslog"
```

**Status:** VERIFIED ✅

---

## Event Log

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{athleteId}/eventlog
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/3054211/eventlog"
```

**Status:** VERIFIED ✅

---

## Player Awards

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{athleteId}/awards
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/3054211/awards"
```

**Status:** PARTIALLY VERIFIED ✅

---

## Player News

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/athletes/{athleteId}/news
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/athletes/3054211/news?limit=10"
```

**Status:** VERIFIED ✅

---

## All Athletes — Core API

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes
```

| Param | Description |
|-------|-------------|
| `active` | `true` for active players only |
| `limit` | Results per page |
| `page` | Page number |
| `position` | Position slug filter |

```bash
# All active players (paginated)
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes?active=true&limit=100"

# Page 2
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes?active=true&limit=100&page=2"
```

**Status:** VERIFIED ✅

---

## Season Athletes — Core API

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/athletes
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/athletes?limit=100"
```

**Status:** VERIFIED ✅

---

## Notable Player IDs

| Player | ESPN ID |
|--------|---------|
| Patrick Mahomes | 3139477 |
| Josh Allen | 3918298 |
| Lamar Jackson | 3916387 |
| Joe Burrow | 3915511 (Baker) / 4361741 (Burrow) |
| Dak Prescott | 3054211 |
| Jalen Hurts | 4040715 |
| Justin Jefferson | 4241389 |
| Tyreek Hill | 3054134 |
| Travis Kelce | 2576980 |
| Micah Parsons | 4241457 |

> Find any player's ESPN ID from their ESPN profile URL:
> `espn.com/nfl/player/_/id/{id}/player-name`
