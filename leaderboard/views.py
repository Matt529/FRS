from django.core.urlresolvers import reverse
from django.db.models import F
from django.shortcuts import render
from .models import TeamLeaderboard


def leaderboard(request):
    top = {
        'All-time Match Wins': (TeamLeaderboard.most_match_wins(1).first(), reverse('team_matches')),
        'All-time Event Wins': (TeamLeaderboard.most_event_wins(1).first(), ''),
        'All-time Highest Win Rate': (TeamLeaderboard.highest_win_rate(1).first(), ''),
        'All-time Elo Leader': (TeamLeaderboard.highest_elo_scaled(1).first(), reverse('team_elo')),
        'All-time Award Wins': (TeamLeaderboard.most_award_wins(1).first(), ''),
        'All-time Blue Banners': (TeamLeaderboard.most_blue_banners(1).first(), ''),
    }

    return render(request, 'leaderboard/leaderboard.html', context={
        'top': top,
    })


def team_elo(request):
    annotated_queryset = TeamLeaderboard.highest_elo_scaled(100).annotate(elo_max=F('elo_mu') + F('elo_sigma'),
                                                                          elo_min=F('elo_mu') - F('elo_sigma'))
    return render(request, 'leaderboard/alltime/team/elo_leaders.html',
                  context={
                      'team_elo': annotated_queryset
                  })


def team_match_wins(request):
    return render(request, 'leaderboard/alltime/team/match_wins.html', context={
        'team_matches': TeamLeaderboard.most_match_wins(100)
    })
