from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from TBAW.models import Team, Event


def landing(request):
    return render(request, 'FRS/landing.html')


def search(request):
    query = request.GET['search']
    team_fields = ('nickname',)
    event_fields = ('event_code',)

    teams = Team.objects.filter(Q(nickname__icontains=query) | Q(key__icontains=query))
    events = Event.objects.filter(Q(key__icontains=query) | Q(name__icontains=query) | Q(short_name__icontains=query))

    resp = serialize('json', list(teams) + list(events), fields=team_fields + event_fields)
    return HttpResponse(resp, content_type='application/json')
