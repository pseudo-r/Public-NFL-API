# Team Endpoints

---

## All Teams

### Site API

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
```

**Status:** VERIFIED ✅

---

### Core API

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams?limit=32"
```

**Status:** VERIFIED ✅

---

## Single Team

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}
```

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
    "nickname": "Chiefs",
    "location": "Kansas City",
    "color": "e31837",
    "alternateColor": "ffb81c",
    "logos": [
      { "href": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png", "width": 500, "height": 500 }
    ],
    "record": { "items": [{ "type": "total", "summary": "15-2", "stats": [] }] },
    "venue": {
      "id": "3636",
      "fullName": "GEHA Field at Arrowhead Stadium",
      "address": { "city": "Kansas City", "state": "MO" },
      "capacity": 76416
    },
    "links": [
      { "rel": ["clubhouse"], "href": "https://www.espn.com/nfl/team/_/name/kc/kansas-city-chiefs" }
    ]
  }
}
```

**Status:** VERIFIED ✅

---

## Team IDs (ESPN)

| Team | ESPN ID | Abbreviation |
|------|---------|--------------|
| Arizona Cardinals | 22 | ARI |
| Atlanta Falcons | 1 | ATL |
| Baltimore Ravens | 33 | BAL |
| Buffalo Bills | 2 | BUF |
| Carolina Panthers | 29 | CAR |
| Chicago Bears | 3 | CHI |
| Cincinnati Bengals | 4 | CIN |
| Cleveland Browns | 5 | CLE |
| Dallas Cowboys | 6 | DAL |
| Denver Broncos | 7 | DEN |
| Detroit Lions | 8 | DET |
| Green Bay Packers | 9 | GB |
| Houston Texans | 34 | HOU |
| Indianapolis Colts | 11 | IND |
| Jacksonville Jaguars | 30 | JAX |
| Kansas City Chiefs | 12 | KC |
| Las Vegas Raiders | 13 | LV |
| Los Angeles Chargers | 24 | LAC |
| Los Angeles Rams | 14 | LAR |
| Miami Dolphins | 15 | MIA |
| Minnesota Vikings | 16 | MIN |
| New England Patriots | 17 | NE |
| New Orleans Saints | 18 | NO |
| New York Giants | 19 | NYG |
| New York Jets | 20 | NYJ |
| Philadelphia Eagles | 21 | PHI |
| Pittsburgh Steelers | 23 | PIT |
| San Francisco 49ers | 25 | SF |
| Seattle Seahawks | 26 | SEA |
| Tampa Bay Buccaneers | 27 | TB |
| Tennessee Titans | 10 | TEN |
| Washington Commanders | 28 | WSH |

---

## Team Roster

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}/roster
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/6/roster"
```

**Response (trimmed):**
```json
{
  "season": { "year": 2025, "type": 4, "name": "Off Season" },
  "athletes": [
    {
      "position": "Quarterback",
      "items": [
        {
          "id": "3054211",
          "fullName": "Dak Prescott",
          "displayName": "Dak Prescott",
          "shortName": "D. Prescott",
          "jersey": "4",
          "position": { "abbreviation": "QB", "name": "Quarterback" },
          "age": 31,
          "experience": { "years": 9 },
          "status": { "name": "Active" }
        }
      ]
    }
  ],
  "coach": [{ "id": "3947", "firstName": "Brian", "lastName": "Schottenheimer" }]
}
```

**Status:** VERIFIED ✅

---

## Team Schedule

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

**Response (trimmed):**
```json
{
  "season": { "year": 2024, "type": 2 },
  "team": { "id": "6", "abbreviation": "DAL", "displayName": "Dallas Cowboys" },
  "events": [
    {
      "id": "401671731",
      "date": "2024-09-08T17:00:00Z",
      "name": "Dallas Cowboys at Cleveland Browns",
      "competitions": [
        {
          "competitors": [
            { "homeAway": "home", "team": { "abbreviation": "CLE" }, "score": "17" },
            { "homeAway": "away", "team": { "abbreviation": "DAL" }, "score": "33" }
          ]
        }
      ]
    }
  ]
}
```

**Status:** VERIFIED ✅

---

## Team Depth Chart

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}/depthcharts
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/6/depthcharts"
```

**Response (trimmed):**
```json
{
  "depthCharts": [
    {
      "name": "Offense",
      "positions": {
        "quarterback": {
          "position": { "name": "Quarterback", "abbreviation": "QB" },
          "athletes": [
            { "rank": 1, "athlete": { "id": "3054211", "displayName": "Dak Prescott" } },
            { "rank": 2, "athlete": { "id": "4360310", "displayName": "Trey Lance" } }
          ]
        }
      }
    }
  ]
}
```

**Status:** VERIFIED ✅

---

## Team Injuries

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}/injuries
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/6/injuries"
```

**Status:** VERIFIED ✅

---

## Team Statistical Leaders

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}/leaders
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/6/leaders"
```

**Status:** VERIFIED ✅

---

## Team News

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{teamId}/news
```

```bash
curl "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/6/news?limit=10"
```

**Status:** VERIFIED ✅

---

## Season-Specific Teams (Core API)

```
GET https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/teams
```

```bash
curl "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/teams?limit=32"
```

**Status:** VERIFIED ✅
