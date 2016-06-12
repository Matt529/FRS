from django.shortcuts import render
from util.getters import get_team
from TBAW.models import Event
from leaderboard.models import TeamLeaderboard


def team_view(request, team_number):
    team = get_team(team_number)
    events = Event.objects.filter(teams__team_number=team.team_number)
    return render(request, 'TBAW/team_view.html',
                  context={
                      'team': team,
                      'events': events,
                  })


def leaderboard(request):
    return render(request, 'TBAW/leaderboard.html',
                  context={
                      'elo_leaders': TeamLeaderboard.highest_elo(100)
                  })
