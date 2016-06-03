from django.core.management.base import BaseCommand
from leaderboard.models import AllianceLeaderboard, TeamLeaderboard


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Most alliance match wins:")
        print(AllianceLeaderboard.most_match_wins(5))
        print("------------------------------------------")

        print("Most 2-way alliance wins:")
        print(AllianceLeaderboard.most_event_wins_2(5))
        print("------------------------------------------")

        print("Most 3-way alliance wins:")
        print(AllianceLeaderboard.most_event_wins_3(5))
        print("------------------------------------------")

        print("Most team match wins:")
        print(TeamLeaderboard.most_match_wins(5))
        print("------------------------------------------")

        print("Most team event wins:")
        print(TeamLeaderboard.most_event_wins(5))
        print("------------------------------------------")
