from time import clock

from TBAW.TBAW_requester import get_list_of_matches_json
from TBAW.models import Match, Alliance, Event
from django.core.management.base import BaseCommand
from util.check import match_exists, alliance_exists
from util.getters import get_team, get_event, get_alliance

matches_created = 0
matches_skipped = 0


def add_all_matches():
    events = Event.objects.all()
    for event in events:
        add_matches_from_event(event.key)


def add_matches_from_event(event_key):
    global matches_created, matches_skipped
    matches = get_list_of_matches_json(event_key)
    print("\tAdding matches from event {0}...".format(event_key))
    for match in matches:
        if match_exists(event_key, match['key']):
            print("Already did this match")
        else:
            red_teams = [get_team(int(x[3:])) for x in match['alliances']['red']['teams']]
            blue_teams = [get_team(int(x[3:])) for x in match['alliances']['blue']['teams']]

            if alliance_exists(red_teams):
                red_alliance = get_alliance(red_teams)
            else:
                red_alliance = Alliance.objects.create()
                red_alliance.color = 'Red'
                red_alliance.save()
                for x in red_teams:
                    red_alliance.teams.add(x)

            if alliance_exists(blue_teams):
                blue_alliance = get_alliance(blue_teams)
            else:
                blue_alliance = Alliance.objects.create()
                blue_alliance.color = 'Blue'
                blue_alliance.save()
                for x in blue_teams:
                    blue_alliance.teams.add(x)

            if match['score_breakdown'] is None:
                print("Skipping match {0} from event {1} (scores not found)".format(match['key'], event_key))
                matches_skipped += 1
                continue

            red_score_breakdown = match['score_breakdown']['red']
            blue_score_breakdown = match['score_breakdown']['blue']

            red_total_points = red_score_breakdown['totalPoints']
            blue_total_points = blue_score_breakdown['totalPoints']
            red_foul_points = red_score_breakdown['foulPoints']
            blue_foul_points = blue_score_breakdown['foulPoints']

            if red_total_points < blue_total_points:
                winner = blue_alliance
            elif red_total_points > blue_total_points:
                winner = red_alliance
            else:
                if red_total_points + red_foul_points > blue_total_points + blue_foul_points:
                    winner = red_alliance
                elif red_total_points + red_foul_points < blue_total_points + blue_foul_points:
                    winner = blue_alliance
                else:
                    winner = None

            match_obj = Match.objects.create(key=match['key'], comp_level=match['comp_level'],
                                             set_number=match['set_number'], match_number=match['match_number'],
                                             event=get_event(event_key), winner=winner)
            match_obj.save()
            match_obj.alliances.add(red_alliance)
            match_obj.alliances.add(blue_alliance)

            matches_created += 1
            print("({7}) Added match {0} ({1}/{2}/{3} vs {4}/{5}/{6})".format(match['key'],
                                                                              red_alliance.teams.all()[0].team_number,
                                                                              red_alliance.teams.all()[1].team_number,
                                                                              red_alliance.teams.all()[2].team_number,
                                                                              blue_alliance.teams.all()[0].team_number,
                                                                              blue_alliance.teams.all()[1].team_number,
                                                                              blue_alliance.teams.all()[2].team_number,
                                                                              matches_created))


class Command(BaseCommand):
    help = "Adds matches to the database"

    def add_arguments(self, parser):
        parser.add_argument('--event', dest='event', default='', type=str)

    def handle(self, *args, **options):
        event = options['event']
        time_start = clock()
        if event is not '':
            add_matches_from_event(event)
        else:
            add_all_matches()
        time_end = clock()
        print("-------------")
        print("Matches created:\t\t{0}".format(matches_created))
        print("Matches skipped:\t\t{0}".format(matches_skipped))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
