from django.core.urlresolvers import reverse
from django.db.models import F
from django.shortcuts import render
from .models import TeamLeaderboard

DEFAULT_SHOW = 100


def leaderboard(request):
    top = {
        'All-time Match Wins': (TeamLeaderboard.most_match_wins(1).first(), reverse('team_matches')),
        'All-time Event Wins': (TeamLeaderboard.most_event_wins(1).first(), reverse('team_events')),
        'All-time Highest Win Rate': (TeamLeaderboard.highest_win_rate(1).first(), reverse('team_winrate')),
        'All-time Elo Leader': (TeamLeaderboard.highest_elo_scaled(1).first(), reverse('team_elo')),
        'All-time Award Wins': (TeamLeaderboard.most_award_wins(1).first(), reverse('team_awards')),
        'All-time Blue Banners': (TeamLeaderboard.most_blue_banners(1).first(), reverse('team_blue_banners')),
    }

    return render(request, 'leaderboard/leaderboard.html', context={
        'top': top,
    })


def team_elo(request):
    annotated_queryset = TeamLeaderboard.highest_elo_scaled(DEFAULT_SHOW).annotate(elo_max=F('elo_mu') + F('elo_sigma'),
                                                                                   elo_min=F('elo_mu') - F('elo_sigma'))
    return render(request, 'leaderboard/alltime/team/elo_leaders.html', context={
        'team_elo': annotated_queryset
    })


def team_match_wins(request):
    return render(request, 'leaderboard/alltime/team/match_wins.html', context={
        'team_matches': TeamLeaderboard.most_match_wins(DEFAULT_SHOW)
    })


def team_event_wins(request):
    return render(request, 'leaderboard/alltime/team/event_wins.html', context={
        'team_events': TeamLeaderboard.most_event_wins(DEFAULT_SHOW)
    })


def team_win_rate(request):
    return render(request, 'leaderboard/alltime/team/winrate.html', context={
        'team_winrate': TeamLeaderboard.highest_win_rate(DEFAULT_SHOW)
    })


def team_award_wins(request):
    return render(request, 'leaderboard/alltime/team/awards.html', context={
        'team_awards': TeamLeaderboard.most_award_wins(DEFAULT_SHOW)
    })


def team_blue_banners(request):
    return render(request, 'leaderboard/alltime/team/blue_banners.html', context={
        'team_blue_banners': TeamLeaderboard.most_blue_banners(DEFAULT_SHOW)
    })
