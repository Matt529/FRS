from TBAW.models import Event
from django.shortcuts import render
from util.getters import get_team, get_event


def team_view(request, team_number):
    team = get_team(team_number)
    events = Event.objects.filter(teams__team_number=team.team_number).order_by('end_date')
    return render(request, 'TBAW/team_view.html',
                  context={
                      'team': team,
                      'events': events,
                  })


def event_view(request, event_key):
    event = get_event(event_key)

    return render(request, 'TBAW/event_view.html',
                  context={
                      'event': event,
                  })
