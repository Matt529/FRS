from django.shortcuts import render
from leaderboard.models import TeamLeaderboard

DEFAULT_SHOW = 200


def team_elo(request):
    return render(request, 'leaderboard/alltime/team/elo_leaders.html', context={
        'team_elo': TeamLeaderboard.highest_elo_scaled(DEFAULT_SHOW)
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
