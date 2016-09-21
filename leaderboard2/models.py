from django.db import models

from TBAW.models import Team


class TeamLeaderboard(models.Model):
    description = models.TextField(default="", null=False)
    field = models.CharField(null=False, max_length=50)
    teams = models.ManyToManyField(Team)
