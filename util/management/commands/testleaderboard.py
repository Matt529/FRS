from pprint import pprint
from time import clock

from django.core.management.base import BaseCommand
from leaderboard.models import OtherLeaderboard, AllianceLeaderboard, TeamLeaderboard, EventLeaderboard


class Command(BaseCommand):
    def handle(self, *args, **options):
        num = 10

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
        pprint(res)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Most team event wins:")
        start = clock()
        res = TeamLeaderboard.most_event_wins(num)
        end = clock()
        pprint(res)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Highest event average match scores:")
        start = clock()
        res = EventLeaderboard.highest_match_average_score(num * 2)
        end = clock()
        pprint(res)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Highest event average playoff match scores:")
        start = clock()
        res = EventLeaderboard.highest_playoff_match_average_score(num * 2)
        end = clock()
        pprint(res)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Highest event average qual match scores:")
        start = clock()
        res = EventLeaderboard.highest_qual_match_average_score(num * 2)
        end = clock()
        pprint(res)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Highest win rate teams:")
        start = clock()
        res = TeamLeaderboard.highest_win_rate(num * 5)
        end = clock()
        pprint(res)
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")

        print("Highest average score region per region:")
        start = clock()
        res = OtherLeaderboard.region_highest_average_score(num)
        end = clock()
        for reg in res:
            print(str(reg).encode('utf-8'))
        print("Operation took {0} seconds".format((end - start).__round__(3)))
        print("------------------------------------------")
