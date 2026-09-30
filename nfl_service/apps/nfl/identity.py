"""Stable transaction identities, independent of local team foreign keys."""

import hashlib
import json


def transaction_identity(nfl_id, date, description, team_id, athlete_id):
    fields = ["nfl", str(nfl_id)] if nfl_id else [
        "natural", str(date or ""), description, str(team_id or ""), str(athlete_id or ""),
    ]
    return hashlib.sha256(json.dumps(fields, ensure_ascii=False).encode()).hexdigest()
