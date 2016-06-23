from django.shortcuts import render
from leaderboard.models import AllianceLeaderboard

DEFAULT_SHOW = 50


def alliance_event_wins_3(request):
    return render(request, 'leaderboard/alltime/alliance/event_wins_3.html', context={
        'alliance_events_3': AllianceLeaderboard.most_event_wins_3(DEFAULT_SHOW)
    })


def alliance_event_wins_2(request):
    return render(request, 'leaderboard/alltime/alliance/event_wins_2.html', context={
        'alliance_events_2': AllianceLeaderboard.most_event_wins_2(DEFAULT_SHOW)
    })
