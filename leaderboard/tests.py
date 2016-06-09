from pprint import pprint
from time import clock

from leaderboard.models import Leaderboard2016, AllianceLeaderboard, TeamLeaderboard


def test_leaderboard(num=10):
    print("Most 2-way alliance match wins:")
    start = clock()
    res = AllianceLeaderboard.most_match_wins_2(num)
    end = clock()
    pprint(res)
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Most 3-way alliance match wins:")
    start = clock()
    res = AllianceLeaderboard.most_match_wins_3(num)
    end = clock()
    pprint(res)
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Most 2-way alliance event wins:")
    start = clock()
    res = AllianceLeaderboard.most_event_wins_2(num)
    end = clock()
    pprint(res)
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Most 3-way alliance event wins:")
    start = clock()
    res = AllianceLeaderboard.most_event_wins_3(num)
    end = clock()
    pprint(res)
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Most team match wins:")
    start = clock()
    res = TeamLeaderboard.most_match_wins(num)
    end = clock()
    for r in res:
        pprint((r, r.num_wins))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Most team event wins:")
    start = clock()
    res = TeamLeaderboard.most_event_wins(num)
    end = clock()
    for r in res:
        pprint((r, r.num_wins))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Highest event average match scores:")
    start = clock()
    res = Leaderboard2016.highest_event_match_average_score(num * 2)
    end = clock()
    for r in res:
        pprint((r, r.avg_score))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Highest win rate teams:")
    start = clock()
    res = TeamLeaderboard.highest_win_rate(num * 5)
    end = clock()
    for r in res:
        pprint((r, r.win_rate))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Ranking Points records")
    start = clock()
    res = Leaderboard2016.highest_team_ranking_points(1.5 * num)
    end = clock()
    for r in res:
        pprint((r, r.ranking_score))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Highest ranking points per game")
    start = clock()
    res = Leaderboard2016.highest_team_ranking_points_per_game(int(1.5 * num))
    end = clock()
    for r in res:
        pprint((r, r.avg_ranking))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Auton records")
    start = clock()
    res = Leaderboard2016.highest_team_auton_points(1.5 * num)
    end = clock()
    for r in res:
        pprint((r, r.auton_points))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Highest auton points per game")
    start = clock()
    res = Leaderboard2016.highest_team_auton_points_per_game(int(1.5 * num))
    end = clock()
    for r in res:
        pprint((r, r.avg_auton))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Scale/Challenge records")
    start = clock()
    res = Leaderboard2016.highest_team_scale_challenge_points(1.5 * num)
    end = clock()
    for r in res:
        pprint((r, r.scale_challenge_points))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Highest scale/challenge points per game")
    start = clock()
    res = Leaderboard2016.highest_team_scale_challenge_points_per_game(int(1.5 * num))
    end = clock()
    for r in res:
        pprint((r, r.avg_scale))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Goals records")
    start = clock()
    res = Leaderboard2016.highest_team_goals_points(1.5 * num)
    end = clock()
    for r in res:
        pprint((r, r.goals_points))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Highest goal points per game")
    start = clock()
    res = Leaderboard2016.highest_team_goals_points_per_game(int(1.5 * num))
    end = clock()
    for r in res:
        pprint((r, r.avg_goals))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Defense records")
    start = clock()
    res = Leaderboard2016.highest_team_defense_points(1.5 * num)
    end = clock()
    for r in res:
        pprint((r, r.defense_points))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Highest defense points per game")
    start = clock()
    res = Leaderboard2016.highest_team_defense_points_per_game(int(1.5 * num))
    end = clock()
    for r in res:
        pprint((r, r.avg_defense))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("OPR records")
    start = clock()
    res = Leaderboard2016.highest_team_opr(1.5 * num)
    end = clock()
    for r in res:
        pprint((r, r.tba_opr))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("DPR records")
    start = clock()
    res = Leaderboard2016.highest_team_dpr(1.5 * num)
    end = clock()
    for r in res:
        pprint((r, r.tba_dpr))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("CCWMS records")
    start = clock()
    res = Leaderboard2016.highest_team_ccwms(1.5 * num)
    end = clock()
    for r in res:
        pprint((r, r.tba_ccwms))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")

    print("Elo Leaders")
    start = clock()
    res = TeamLeaderboard.highest_elo(num * 2)
    end = clock()
    for r in res:
        pprint((r, r.elo_mu))
    print("Operation took {0} seconds".format((end - start).__round__(3)))
    print("------------------------------------------")
