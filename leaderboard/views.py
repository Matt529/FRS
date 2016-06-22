from django.core.urlresolvers import reverse
from django.db.models import F
from django.shortcuts import render
from .models import TeamLeaderboard


def leaderboard(request):
    top = {
        'All-time Match Wins': (TeamLeaderboard.most_match_wins(1).first(), ''),
        'All-time Event Wins': (TeamLeaderboard.most_event_wins(1).first(), ''),
        'All-time Highest Win Rate': (TeamLeaderboard.highest_win_rate(1).first(), ''),
        'All-time Elo Leader': (TeamLeaderboard.highest_elo_scaled(1).first(), '{}'.format(reverse('elo_leaders'))),
        'All-time Award Wins': (TeamLeaderboard.most_award_wins(1).first(), ''),
        'All-time Blue Banners': (TeamLeaderboard.most_blue_banners(1).first(), ''),
    }

    return render(request, 'leaderboard/leaderboard.html', context={
        'top': top,
    })


def elo_leaders(request):
    annotated_queryset = TeamLeaderboard.highest_elo_scaled(100).annotate(elo_max=F('elo_mu') + F('elo_sigma'),
                                                                          elo_min=F('elo_mu') - F('elo_sigma'))
    return render(request, 'leaderboard/elo_leaders.html',
                  context={
                      'elo_leaders': annotated_queryset
                  })
