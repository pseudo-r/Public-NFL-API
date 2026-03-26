# League Endpoints

> **⚠️ Bearer Token Required:** All endpoints return 401 Unauthorized without a valid `Authorization: Bearer {token}` header.

---

## Standings

```
GET https://api.nfl.com/v1/standings
```

| Param | Description |
|-------|-------------|
| `season` | Year |
| `seasonType` | `REG` , `PRE` |

```bash
curl "https://api.nfl.com/v1/standings?season=2024&seasonType=REG" \
  -H "Authorization: Bearer <your_token>"
```

**Status:** AUTH LOCKED 🔒

---

## Seasons

```
GET https://api.nfl.com/v1/seasons
```

Retrieves metadata about current and historical seasons, including start dates and weeks.

```bash
curl "https://api.nfl.com/v1/seasons" \
  -H "Authorization: Bearer <your_token>"
```

**Status:** AUTH LOCKED 🔒

---

## Shield / GraphQL Node

The NFL is slowly transitioning much of its REST functionality to a federated GraphQL endpoint known as `shield`. 

```
POST https://api.nfl.com/v3/shield/
```

```bash
curl -X POST "https://api.nfl.com/v3/shield/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { id } }"}'
```

**Status:** AUTH LOCKED 🔒
