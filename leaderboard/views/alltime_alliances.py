from django.shortcuts import render
from leaderboard.models import AllianceLeaderboard
from util.getters import reverse_model_url

DEFAULT_SHOW = 100


def alliance_event_wins_3(request):
    return render(request, 'leaderboard/alltime/alliance/event_wins_3.html', context={
        'alliance_events_3': AllianceLeaderboard.most_event_wins_3(DEFAULT_SHOW)
    })


def alliance_event_wins_2(request):
    return render(request, 'leaderboard/alltime/alliance/event_wins_2.html', context={
        'alliance_events_2': AllianceLeaderboard.most_event_wins_2(DEFAULT_SHOW)
    })


def alliance_match_wins_3(request):
    return render(request, 'leaderboard/alltime/alliance/match_wins_3.html', context={
        'alliance_matches_3': AllianceLeaderboard.most_match_wins_3(DEFAULT_SHOW)
    })


def alliance_elo(request):
    return render(request, 'leaderboard/alltime/alliance/elo.html', context={
        'alliance_elo': AllianceLeaderboard.highest_elo(DEFAULT_SHOW)
    })


def __make_alliance_tr(name, url, holder_alliance, stat):
    teams = holder_alliance.teams.all()
    return {
        'name': name,
        'url': url,
        'holder': ', '.join(map(str, teams)),
        'holder_url': reverse_model_url(holder_alliance),
        'stat': stat
    }
