# Player Endpoints

> **⚠️ Bearer Token Required:** All endpoints return 401 Unauthorized without a valid `Authorization: Bearer {token}` header.

---

## All Players

```
GET https://api.nfl.com/v1/players
```

| Param | Description |
|-------|-------------|
| `limit` | Pagination limit |
| `offset` | Pagination offset |

```bash
curl "https://api.nfl.com/v1/players?limit=100" \
  -H "Authorization: Bearer <your_token>"
```

**Status:** AUTH LOCKED 🔒

---

## Single Player Profile

```
GET https://api.nfl.com/v1/players/{playerId}
```

```bash
# Get details for player by their NFL Global ID
curl "https://api.nfl.com/v1/players/32004252-4131-6450-0000-000000000000" \
  -H "Authorization: Bearer <your_token>"
```

**Status:** AUTH LOCKED 🔒

---

## Player Statistics (Season)

```
GET https://api.nfl.com/v1/players/{playerId}/stats
```

| Param | Description |
|-------|-------------|
| `season` | Numeric Year |
| `seasonType` | `REG`, `POST`, `PRE` |

```bash
curl "https://api.nfl.com/v1/players/32004252.../stats?season=2024&seasonType=REG" \
  -H "Authorization: Bearer <your_token>"
```

**Status:** AUTH LOCKED 🔒

---

## Native NFL Player IDs

The official `api.nfl.com` player endpoint requires an NFL Global ID (UUID/GUID format). These IDs differ completely from standard numeric IDs used by fantasy portals or ESPN. 

Example NFL Player ID format:
`32004252-4131-6450-0000-000000000000`
