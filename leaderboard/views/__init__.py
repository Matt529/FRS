from django.core.urlresolvers import reverse
from .alltime_alliances import *
from .alltime_teams import *


def leaderboard(request):
    team_top = {
        'All-time Match Wins': (TeamLeaderboard.most_match_wins(1).first(), reverse('team_matches')),
        'All-time Event Wins': (TeamLeaderboard.most_event_wins(1).first(), reverse('team_events')),
        'All-time Highest Win Rate': (TeamLeaderboard.highest_win_rate(1).first(), reverse('team_winrate')),
        'All-time Elo Leader': (TeamLeaderboard.highest_elo_scaled(1).first(), reverse('team_elo')),
        'All-time Award Wins': (TeamLeaderboard.most_award_wins(1).first(), reverse('team_awards')),
        'All-time Blue Banners': (TeamLeaderboard.most_blue_banners(1).first(), reverse('team_blue_banners')),
    }

    alliance_top = {
        'All-time Event Wins (3)': (AllianceLeaderboard.most_event_wins_3(1), reverse('alliance_events_3')),
        'All-time Event Wins (2)': (AllianceLeaderboard.most_event_wins_2(1), reverse('alliance_events_2')),
    }

    return render(request, 'leaderboard/leaderboard.html', context={
        'team_top': team_top,
        'alliance_top': alliance_top,
    })
