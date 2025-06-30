from datetime import date
import logging

from app import db
from app.models import AthleteProfile, NBATeam, NHLTeam
from app.services import nba_service, nfl_service, mlb_service, nhl_service

logger = logging.getLogger(__name__)


def nightly_sync_games():
    """Sync team lists and game results for the current season."""
    year = date.today().year

    nba_client = nba_service.NBAAPIClient()
    nba_service.sync_teams(nba_client)
    for team in NBATeam.query.all():
        nba_service.sync_games(nba_client, team.team_id, season=year)

    nhl_client = nhl_service.NHLAPIClient()
    nhl_service.sync_teams(nhl_client)
    for team in NHLTeam.query.all():
        nhl_service.sync_games(nhl_client, team.team_id, season=str(year))

    logger.info("Nightly game sync complete")


def weekly_sync_player_stats():
    """Update player statistics across all sports."""
    year = date.today().year

    nba_client = nba_service.NBAAPIClient()
    nfl_client = nfl_service.NFLAPIClient()
    mlb_client = mlb_service.MLBAPIClient()
    nhl_client = nhl_service.NHLAPIClient()

    for athlete in AthleteProfile.query.all():
        sport = athlete.primary_sport.code if athlete.primary_sport else None
        if sport == "NBA":
            nba_service.sync_player_stats(nba_client, athlete, season=year)
        elif sport == "NFL":
            nfl_service.sync_player_stats(nfl_client, athlete, season=year)
        elif sport == "MLB":
            mlb_service.sync_player_stats(mlb_client, athlete, season=year)
        elif sport == "NHL":
            nhl_service.sync_player_stats(nhl_client, athlete, season=str(year))

    logger.info("Weekly player stats sync complete")

