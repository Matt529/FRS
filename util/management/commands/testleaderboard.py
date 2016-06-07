from pprint import pprint
from time import clock

from django.core.management.base import BaseCommand
from leaderboard.year_leaderboard_models import Leaderboard2016


class Command(BaseCommand):
    def handle(self, *args, **options):
        num = 10

        # print("Most 2-way alliance match wins:")
        # start = clock()
        # res = AllianceLeaderboard.most_match_wins_2(num)
        # end = clock()
        # pprint(res)
        # print("Operation took {0} seconds".format((end - start).__round__(3)))
        # print("------------------------------------------")
        #
        # print("Most 3-way alliance match wins:")
        # start = clock()
        # res = AllianceLeaderboard.most_match_wins_3(num)
        # end = clock()
        # pprint(res)
        # print("Operation took {0} seconds".format((end - start).__round__(3)))
        # print("------------------------------------------")
        #
        # print("Most 2-way alliance event wins:")
        # start = clock()
        # res = AllianceLeaderboard.most_event_wins_2(num)
        # end = clock()
        # pprint(res)
        # print("Operation took {0} seconds".format((end - start).__round__(3)))
        # print("------------------------------------------")
        #
        # print("Most 3-way alliance event wins:")
        # start = clock()
        # res = AllianceLeaderboard.most_event_wins_3(num)
        # end = clock()
        # pprint(res)
        # print("Operation took {0} seconds".format((end - start).__round__(3)))
        # print("------------------------------------------")
        #
        # print("Most team match wins:")
        # start = clock()
        # res = TeamLeaderboard.most_match_wins(num)
        # end = clock()
        # pprint(res)
        # print("Operation took {0} seconds".format((end - start).__round__(3)))
        # print("------------------------------------------")
        #
        # print("Most team event wins:")
        # start = clock()
        # res = TeamLeaderboard.most_event_wins(num)
        # end = clock()
        # pprint(res)
        # print("Operation took {0} seconds".format((end - start).__round__(3)))
        # print("------------------------------------------")
        #
        # print("Highest event average match scores:")
        # start = clock()
        # res = EventLeaderboard.highest_match_average_score(num * 2)
        # end = clock()
        # pprint(res)
        # print("Operation took {0} seconds".format((end - start).__round__(3)))
        # print("------------------------------------------")
        #
        # print("Highest event average playoff match scores:")
        # start = clock()
        # res = EventLeaderboard.highest_playoff_match_average_score(num * 2)
        # end = clock()
        # pprint(res)
        # print("Operation took {0} seconds".format((end - start).__round__(3)))
        # print("------------------------------------------")
        #
        # print("Highest event average qual match scores:")
        # start = clock()
        # res = EventLeaderboard.highest_qual_match_average_score(num * 2)
        # end = clock()
        # pprint(res)
        # print("Operation took {0} seconds".format((end - start).__round__(3)))
        # print("------------------------------------------")
        #
        # print("Highest win rate teams:")
        # start = clock()
        # res = TeamLeaderboard.highest_win_rate(num * 5)
        # end = clock()
        # pprint(res)
        # print("Operation took {0} seconds".format((end - start).__round__(3)))
        # print("------------------------------------------")
        #
        # print("Highest average score region per region:")
        # start = clock()
        # res = OtherLeaderboard.region_highest_average_score(num)
        # end = clock()
        # for reg in res:
        #     print(str(reg).encode('utf-8'))
        # print("Operation took {0} seconds".format((end - start).__round__(3)))
        # print("------------------------------------------")

        print("Ranking Points records")
        start = clock()
        res = Leaderboard2016.highest_ranking_points(1.5 * num)
        end = clock()
        rs = []
        for r in res:
            rs.append([r.team, r.event, r.ranking_score])
        pprint(rs)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Highest ranking points per game")
        start = clock()
        res = Leaderboard2016.highest_ranking_points_per_game(int(1.5 * num))
        end = clock()
        pprint(res)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Auton records")
        start = clock()
        res = Leaderboard2016.highest_auton_points(1.5 * num)
        end = clock()
        rs = []
        for r in res:
            rs.append([r.team, r.event, r.auton_points])
        pprint(rs)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Highest auton points per game")
        start = clock()
        res = Leaderboard2016.highest_auton_points_per_game(int(1.5 * num))
        end = clock()
        pprint(res)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Scale/Challenge records")
        start = clock()
        res = Leaderboard2016.highest_scale_challenge_points(1.5 * num)
        end = clock()
        rs = []
        for r in res:
            rs.append([r.team, r.event, r.scale_challenge_points])
        pprint(rs)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Highest scale/challenge points per game")
        start = clock()
        res = Leaderboard2016.highest_scale_challenge_points_per_game(int(1.5 * num))
        end = clock()
        pprint(res)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Goals records")
        start = clock()
        res = Leaderboard2016.highest_goals_points(1.5 * num)
        end = clock()
        rs = []
        for r in res:
            rs.append([r.team, r.event, r.goals_points])
        pprint(rs)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Highest goal points per game")
        start = clock()
        res = Leaderboard2016.highest_goals_points_per_game(int(1.5 * num))
        end = clock()
        pprint(res)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Defense records")
        start = clock()
        res = Leaderboard2016.highest_defense_points(1.5 * num)
        end = clock()
        rs = []
        for r in res:
            rs.append([r.team, r.event, r.defense_points])
        pprint(rs)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Highest defense points per game")
        start = clock()
        res = Leaderboard2016.highest_defense_points_per_game(int(1.5 * num))
        end = clock()
        pprint(res)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("OPR records")
        start = clock()
        res = Leaderboard2016.highest_opr(1.5 * num)
        end = clock()
        rs = []
        for r in res:
            rs.append([r.team, r.event, r.tba_opr])
        pprint(rs)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("DPR records")
        start = clock()
        res = Leaderboard2016.highest_dpr(1.5 * num)
        end = clock()
        rs = []
        for r in res:
            rs.append([r.team, r.event, r.tba_dpr])
        pprint(rs)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("CCWMS records")
        start = clock()
        res = Leaderboard2016.highest_ccwms(1.5 * num)
        end = clock()
        rs = []
        for r in res:
            rs.append([r.team, r.event, r.tba_ccwms])
        pprint(rs)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")
