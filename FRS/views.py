from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from TBAW.models import Team, Event
from util.getters import reverse_model_url


def landing(request):
    return render(request, 'FRS/landing.html')


def search(request):
    query = request.GET['search']

    teams = Team.objects.filter(Q(nickname__icontains=query) | Q(key__icontains=query))
    events = Event.objects.filter(Q(key__icontains=query) | Q(name__icontains=query) | Q(short_name__icontains=query))

    if teams.count() > 0:
        return HttpResponseRedirect(reverse_model_url(teams.first()))
    elif events.count() > 0:
        return HttpResponseRedirect(reverse_model_url(events.first()))
    else:
        return render(request, 'FRS/search_found_nothing.html', {'query': query})


def search_api(request):
    query = request.GET['search']
    team_fields = ('nickname',)
    event_fields = ('event_code',)

    teams = Team.objects.filter(Q(nickname__icontains=query) | Q(key__icontains=query))
    events = Event.objects.filter(Q(key__icontains=query) | Q(name__icontains=query) | Q(short_name__icontains=query))

    resp = serialize('json', list(teams) + list(events), fields=team_fields + event_fields)
    return HttpResponse(resp, content_type='application/json')
