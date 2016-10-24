from .alltime_alliances import *
from .alltime_teams import *
from .years import *


def leaderboard(request):
    team_most_match_wins = TeamLeaderboard.most_match_wins(1).first()
    team_most_event_wins = TeamLeaderboard.most_event_wins(1).first()
    team_highest_win_rate = TeamLeaderboard.highest_win_rate(1).first()
    team_highest_elo = TeamLeaderboard.highest_elo(1).first()
    team_most_award_wins = TeamLeaderboard.most_award_wins(1).first()
    team_most_blue_banner_wins = TeamLeaderboard.most_blue_banners(1).first()
    team_longest_recorded_streak = TeamLeaderboard.longest_recorded_event_winstreak(1).first()
    team_longest_active_streak = TeamLeaderboard.longest_active_event_winstreak(1).first()

    team_top = [
        make_team_table_row('All-time Match Wins', reverse('team_matches'), team_most_match_wins,
                            team_most_match_wins.match_wins),
        make_team_table_row('All-time Event Wins', reverse('team_events'), team_most_event_wins,
                            team_most_event_wins.event_wins),
        make_team_table_row('All-time Win Rate', reverse('team_winrate'), team_highest_win_rate,
                            team_highest_win_rate.win_rate),
        make_team_table_row('All-time Elo (Team)', reverse('team_elo'), team_highest_elo,
                            team_highest_elo.elo_mu),
        make_team_table_row('All-time Award Wins', reverse('team_awards'), team_most_award_wins,
                            team_most_award_wins.award_wins),
        make_team_table_row('All-time Blue Banners', reverse('team_blue_banners'), team_most_blue_banner_wins,
                            team_most_blue_banner_wins.blue_banners_won),
        make_team_table_row('Longest Recorded Event Winstreak', reverse('team_longest_winstreak'),
                            team_longest_recorded_streak, team_longest_recorded_streak.longest_event_winstreak),
        make_team_table_row('Longest Active Event Winstreak', reverse('team_active_winstreak'),
                            team_longest_active_streak, team_longest_active_streak.active_event_winstreak),
    ]

    alliance_most_match_wins_3 = AllianceLeaderboard.most_match_wins_3(1).first()
    alliance_most_event_wins_3 = AllianceLeaderboard.most_event_wins_3(1).first()
    alliance_highest_elo = AllianceLeaderboard.highest_elo(1).first()

    alliance_top = [
        __make_alliance_tr('All-time Match Wins (3)', reverse('alliance_matches_3'), alliance_most_match_wins_3,
                           alliance_most_match_wins_3.match_wins),
        __make_alliance_tr('All-time Event Wins (3)', reverse('alliance_events_3'), alliance_most_event_wins_3,
                           alliance_most_event_wins_3.event_wins),
        __make_alliance_tr('All-time Elo (Alliance)', reverse('alliance_elo'), alliance_highest_elo,
                           alliance_highest_elo.elo_mu)
    ]

    return render(request, 'leaderboard/leaderboard.html', context={
        'leaderboard': team_top + alliance_top
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
