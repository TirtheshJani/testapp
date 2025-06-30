import logging
from typing import Optional

import requests
from flask import current_app

from app import db
from app.models import MLBTeam, AthleteProfile, AthleteStat
from .data_mapping import map_mlb_team


class MLBAPIClient:
    """Client for the public MLB stats API."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or current_app.config.get(
            "MLB_API_BASE_URL", "https://statsapi.mlb.com/api/v1"
        )
        self.session = requests.Session()

    def _get(self, endpoint: str, params: Optional[dict] = None):
        url = f"{self.base_url}{endpoint}"
        resp = self.session.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_teams(self):
        data = self._get("/teams")
        return data.get("teams", [])

    def get_player_stats(self, player_id: int, season: Optional[int] = None, group: str = "hitting"):
        params = {"stats": "season", "group": group}
        if season:
            params["season"] = season
        data = self._get(f"/people/{player_id}/stats", params=params)
        if data.get("stats"):
            splits = data["stats"][0].get("splits", [])
            if splits:
                return splits[0].get("stat", {})
        return None


def sync_teams(client: MLBAPIClient):
    """Fetch and store all MLB teams."""
    teams = client.get_teams()
    for t in teams:
        mapped = map_mlb_team(t)
        team = MLBTeam.query.get(mapped["team_id"])
        if not team:
            team = MLBTeam(team_id=mapped["team_id"])
        team.name = mapped["name"]
        team.abbreviation = mapped["abbreviation"]
        team.location = mapped["location"]
        team.league = mapped["league"]
        team.division = mapped["division"]
        db.session.add(team)
    db.session.commit()
    logging.getLogger(__name__).info("Synced %d MLB teams", len(teams))
    return teams


def sync_player_stats(client: MLBAPIClient, athlete: AthleteProfile, season: Optional[int] = None):
    """Fetch MLB stats for an athlete and store them."""
    player_id = getattr(athlete, "mlb_player_id", None)
    if not player_id:
        return None

    hitting = client.get_player_stats(player_id, season=season, group="hitting") or {}
    pitching = client.get_player_stats(player_id, season=season, group="pitching") or {}
    fielding = client.get_player_stats(player_id, season=season, group="fielding") or {}

    mappings = {
        "MLB_HITTING": {"avg": "BattingAverage"},
        "MLB_PITCHING": {"era": "EarnedRunAverage"},
        "MLB_FIELDING": {"fielding": "FieldingPercentage"},
    }

    season_str = str(season) if season else None

    for stat_type, mapping in mappings.items():
        source = {
            "MLB_HITTING": hitting,
            "MLB_PITCHING": pitching,
            "MLB_FIELDING": fielding,
        }[stat_type]
        for api_field, stat_name in mapping.items():
            if api_field not in source:
                continue
            stat = AthleteStat.query.filter_by(
                athlete_id=athlete.athlete_id,
                name=stat_name,
                season=season_str,
            ).first()
            if not stat:
                stat = AthleteStat(
                    athlete_id=athlete.athlete_id,
                    name=stat_name,
                    season=season_str,
                )
            stat.value = str(source.get(api_field))
            stat.stat_type = stat_type
            db.session.add(stat)

    db.session.commit()
    logging.getLogger(__name__).info(
        "Synced MLB stats for athlete %s season %s", athlete.athlete_id, season_str
    )
    return {
        "hitting": hitting,
        "pitching": pitching,
        "fielding": fielding,
    }
