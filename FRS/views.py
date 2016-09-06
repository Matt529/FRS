from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from TBAW.models import Team, Event
from util.getters import reverse_model_url


def landing(request):
    return render(request, 'FRS/landing.html')


def search(request):
    query = request.POST['search']
    teams = Team.objects.filter(Q(name__icontains=query) | Q(nickname__icontains=query) | Q(key__icontains=query))
    if teams.exists():
        return HttpResponseRedirect(reverse_model_url(teams[0]))

    events = Event.objects.filter(Q(key__icontains=query) | Q(name__icontains=query) | Q(short_name__icontains=query))
    if events.exists():
        return HttpResponseRedirect(reverse_model_url(events[0]))

    return render(request, 'FRS/landing.html')
