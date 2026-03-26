# Game Endpoints

All endpoints on this page return NFL game data from the native `api.nfl.com` service. 

> **⚠️ Bearer Token Required:** All endpoints return 401 Unauthorized without a valid `Authorization: Bearer {token}` header.

---

## Scoreboard

```
GET https://api.nfl.com/v1/games
```

| Param | Description | Example |
|-------|-------------|---------|
| `season` | Year | `2024` |
| `seasonType` | `PRE`, `REG`, `POST` | `REG` |
| `week` | NFL week | `1`–`18` |

```bash
# Week 18, 2024 regular season
curl "https://api.nfl.com/v1/games?season=2024&seasonType=REG&week=18" \
  -H "Authorization: Bearer <your_token>"
```

**Status:** AUTH LOCKED 🔒

---

## Single Game Detail

```
GET https://api.nfl.com/v1/games/{gameId}
```

> **Note on NFL Game IDs:** The native NFL game ID format is `{YYYYMMDD}{homeTeam3DigitId}` (e.g. `20240105027` for TB at home).

```bash
curl "https://api.nfl.com/v1/games/20240105027" \
  -H "Authorization: Bearer <your_token>"
```

**Status:** AUTH LOCKED 🔒

---

## Game Drives & Plays

The REST endpoints for play-by-play have largely been shifted to GraphQL in recent years, but legacy v1 properties remain on the mobile API.

```
GET https://api.nfl.com/v1/games/{gameId}/plays
```

| Param | Description |
|-------|-------------|
| `limit` | Max plays to return |
| `offset` | Pagination |

```bash
curl "https://api.nfl.com/v1/games/20240105027/plays?limit=100" \
  -H "Authorization: Bearer <your_token>"
```

**Status:** AUTH LOCKED 🔒

---

## Next Gen Stats: Passing (Live)

```
GET https://nextgenstats.nfl.com/api/statboard/passing
```

| Param | Description | Example |
|-------|-------------|---------|
| `season` | Year | `2024` |
| `seasonType` | `REG`, `PRE`, `POST` | `REG` |
| `week` | Week number | `18` |

```bash
curl "https://nextgenstats.nfl.com/api/statboard/passing?season=2024&seasonType=REG&week=18" \
  -H "Cookie: _gcl_au=... [NFL.com Session Cookie Required]"
```

**Status:** AUTH LOCKED 🔒
