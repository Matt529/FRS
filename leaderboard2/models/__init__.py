from django.db.models.signals import m2m_changed

from .leaderboards import TeamLeaderboard
from .signals import team_leaderboard_changed

m2m_changed.connect(team_leaderboard_changed, sender=TeamLeaderboard.teams.through)
