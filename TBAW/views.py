from TBAW.models import Event, Team, RankingModel
from django.shortcuts import render
from util.check import alliance_exists, team_exists
from util.getters import get_team, get_event, get_alliance


def team_view(request, team_number):
    team = get_team(team_number)
    events = Event.objects.filter(teams__team_number=team.team_number).order_by('end_date')
    awards_count = team.get_awards().count()

    return render(request, 'TBAW/team_view.html',
                  context={
                      'team': team,
                      'events': events,
                      'awards_count': awards_count,
                  })


def event_view(request, event_key):
    event = get_event(event_key)
    ranking_models = RankingModel.objects.filter(event=event)

    return render(request, 'TBAW/event_view.html',
                  context={
                      'event': event,
                      'ranking_models': ranking_models,
                  })


def alliance_view(request, team1, team2, team3):
    if team_exists(team1):
        team1 = get_team(team1)
    if team_exists(team2):
        team2 = get_team(team2)
    if team_exists(team3):
        team3 = get_team(team3)

    if type(team1) is Team and type(team2) is Team and type(team3) is Team and alliance_exists([team1, team2, team3]):
        return alliance_exists_view(request, get_alliance([team1, team2, team3]))
    else:
        return alliance_does_not_exist_view(request, [team1, team2, team3])


def alliance_view_alliance_obj(request, alliance_obj):
    teams = alliance_obj.teams.all()
    return alliance_view(request, teams[0].team_number, teams[1].team_number, teams[2].team_number)


def alliance_exists_view(request, alliance):
    events = Event.objects.filter(allianceappearance__alliance=alliance).order_by('-end_date')
    wins = alliance.get_wins()
    losses = alliance.get_losses()
    ties = alliance.get_ties()

    return render(request, 'TBAW/alliance_exists.html', context={
        'alliance': alliance,
        'events': events,
    })


def alliance_does_not_exist_view(request, teams):
    return render(request, 'TBAW/alliance_does_not_exist.html', context={
        'teams': teams
    })
