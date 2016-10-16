import random

from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from TBAW.models import Team, Event
from util.getters import reverse_model_url
from util.viewutils import require_http_methods_plus


def handle_404(request):
    gifs = [
        '//zippy.gfycat.com/BeneficialSingleCurassow.webm',
        '//i.imgur.com/7mtLFpn.mp4',
        '//i.imgur.com/dEYwB1V.mp4',
        '//i.imgur.com/nhklRqC.mp4',
        '//fat.gfycat.com/MintyCelebratedFirefly.webm',
        '//zippy.gfycat.com/BleakDeadHammerheadshark.webm',
        '//i.imgur.com/LV3Qc1H.mp4',
        '//i.imgur.com/1Yfuwrn.mp4',
        '//i.imgur.com/2wU3y70.mp4',
    ]

    response = render_to_response('FRS/404.html', context={
        'webm': random.choice(gifs),
    }, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def landing(request):
    return render(request, 'FRS/landing.html')


@require_http_methods_plus(['GET'])
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


@require_http_methods_plus(['GET'])
def search_api(request):
    query = request.GET['search']
    team_fields = ('nickname',)
    event_fields = ('event_code',)

    teams = Team.objects.filter(Q(nickname__icontains=query) | Q(key__icontains=query))
    events = Event.objects.filter(Q(key__icontains=query) | Q(name__icontains=query) | Q(short_name__icontains=query))

    resp = serialize('json', list(teams) + list(events), fields=team_fields + event_fields)
    return HttpResponse(resp, content_type='application/json')
