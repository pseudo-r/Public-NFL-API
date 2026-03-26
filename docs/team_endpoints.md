# Team Endpoints

> **⚠️ Bearer Token Required:** All endpoints return 401 Unauthorized without a valid `Authorization: Bearer {token}` header.

---

## All Teams

```
GET https://api.nfl.com/v1/teams
```

```bash
curl "https://api.nfl.com/v1/teams" \
  -H "Authorization: Bearer <your_token>"
```

**Status:** AUTH LOCKED 🔒

---

## Single Team

```
GET https://api.nfl.com/v1/teams/{teamId}
```

```bash
# Get details for team 'KC' (Kansas City Chiefs)
curl "https://api.nfl.com/v1/teams/KC" \
  -H "Authorization: Bearer <your_token>"
```

**Status:** AUTH LOCKED 🔒

---

## Team Roster

```
GET https://api.nfl.com/v1/teams/{teamId}/roster
```

```bash
curl "https://api.nfl.com/v1/teams/DAL/roster" \
  -H "Authorization: Bearer <your_token>"
```

**Status:** AUTH LOCKED 🔒

---

## Native NFL Team IDs

Unlike ESPN (which uses numeric IDs like `12`), the native `api.nfl.com` endpoints often use standard 2- or 3-letter abbreviations (`KC`, `DAL`, `TB`, `SF`).

| Team | Native ID |
|------|-----------|
| Dallas Cowboys | DAL |
| Kansas City Chiefs | KC |
| Tampa Bay Buccaneers | TB |
| San Francisco 49ers | SF |
| Buffalo Bills | BUF |
| Baltimore Ravens | BAL |
