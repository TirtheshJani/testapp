import logging
from datetime import datetime
from typing import Optional

import requests
from flask import current_app

from app import db
from app.models import NHLTeam, NHLGame, AthleteProfile, AthleteStat


class NHLAPIClient:
    """Client for the public NHL stats API."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or current_app.config.get(
            "NHL_API_BASE_URL", "https://statsapi.web.nhl.com/api/v1"
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

    def get_standings(self):
        data = self._get("/standings")
        return data.get("records", [])

    def get_games(self, team_id: int, season: Optional[str] = None):
        params = {"teamId": team_id}
        if season:
            params["season"] = season
        data = self._get("/schedule", params=params)
        games = []
        for d in data.get("dates", []):
            games.extend(d.get("games", []))
        return games

    def get_player_stats(self, player_id: int, season: Optional[str] = None):
        params = {"stats": "statsSingleSeason"}
        if season:
            params["season"] = season
        data = self._get(f"/people/{player_id}/stats", params=params)
        if data.get("stats"):
            splits = data["stats"][0].get("splits", [])
            if splits:
                return splits[0].get("stat", {})
        return None


def sync_teams(client: NHLAPIClient):
    """Fetch and store all NHL teams."""
    teams = client.get_teams()
    for t in teams:
        team = NHLTeam.query.get(t["id"])
        if not team:
            team = NHLTeam(team_id=t["id"])
        team.name = t.get("name")
        team.abbreviation = t.get("abbreviation")
        team.location = t.get("locationName") or t.get("teamName")
        team.division = (t.get("division") or {}).get("name")
        team.conference = (t.get("conference") or {}).get("name")
        db.session.add(team)
    db.session.commit()
    logging.getLogger(__name__).info("Synced %d NHL teams", len(teams))
    return teams


def sync_standings(client: NHLAPIClient):
    """Fetch standings and update team records."""
    records = client.get_standings()
    for r in records:
        for tr in r.get("teamRecords", []):
            team_id = tr["team"]["id"]
            team = NHLTeam.query.get(team_id)
            if not team:
                continue
            league = tr.get("leagueRecord", {})
            team.wins = league.get("wins")
            team.losses = league.get("losses")
            team.overtime_losses = league.get("ot")
            team.points = tr.get("points")
            db.session.add(team)
    db.session.commit()
    logging.getLogger(__name__).info("Synced NHL standings")
    return records


def sync_games(client: NHLAPIClient, team_id: int, season: Optional[str] = None):
    """Fetch schedule for a team and store the games."""
    games = client.get_games(team_id=team_id, season=season)
    for g in games:
        game_id = g["gamePk"]
        game = NHLGame.query.get(game_id)
        if not game:
            game = NHLGame(game_id=game_id)
        game.date = datetime.fromisoformat(g["gameDate"].rstrip("Z")).date()
        game.season = g.get("season")
        game.home_team_id = g["teams"]["home"]["team"]["id"]
        game.visitor_team_id = g["teams"]["away"]["team"]["id"]
        game.home_team_score = g["teams"]["home"].get("score")
        game.visitor_team_score = g["teams"]["away"].get("score")
        db.session.add(game)
    db.session.commit()
    logging.getLogger(__name__).info(
        "Synced %d NHL games for team %s", len(games), team_id
    )
    return games


def sync_player_stats(
    client: NHLAPIClient, athlete: AthleteProfile, season: Optional[str] = None
):
    """Fetch NHL stats for an athlete and store them."""
    player_id = getattr(athlete, "nhl_player_id", None)
    if not player_id:
        return None

    data = client.get_player_stats(player_id, season=season) or {}

    mapping = {"goals": "Goals", "assists": "Assists", "points": "Points"}
    season_str = str(season) if season else None

    for api_field, stat_name in mapping.items():
        if api_field not in data:
            continue
        stat = AthleteStat.query.filter_by(
            athlete_id=athlete.athlete_id, name=stat_name, season=season_str
        ).first()
        if not stat:
            stat = AthleteStat(
                athlete_id=athlete.athlete_id, name=stat_name, season=season_str
            )
        stat.value = str(data.get(api_field))
        stat.stat_type = "NHL"
        db.session.add(stat)

    db.session.commit()
    logging.getLogger(__name__).info(
        "Synced NHL stats for athlete %s season %s", athlete.athlete_id, season_str
    )
    return data
