from TBAW.TBAW_requester import get_list_of_matches_json
from TBAW.models import Alliance, Match
from django.core.management.base import BaseCommand
from util.check import match_exists
from util.getters import get_team, get_event

matches_added = 0
matches_updated = 0


def add_matches_from_event(event_key):
    global matches_added, matches_updated
    matches = get_list_of_matches_json(event_key)
    for match in matches:
        if match_exists(event_key, match['key']):
            pass
        else:
            red_alliance = Alliance.objects.create()
            red_alliance.color = 'Red'
            red_alliance.save()
            for team_key in match['alliances']['red']['teams']:
                red_alliance.teams.add(get_team(int(team_key[3:])))

            blue_alliance = Alliance.objects.create()
            blue_alliance.color = 'Blue'
            blue_alliance.save()
            for team_key in match['alliances']['blue']['teams']:
                blue_alliance.teams.add(get_team(int(team_key[3:])))

            match_obj = Match.objects.create(key=match['key'], comp_level=match['comp_level'],
                                             set_number=match['set_number'], match_number=match['match_number'],
                                             event=get_event(event_key))
            match_obj.save()
            match_obj.alliances.add(red_alliance)
            match_obj.alliances.add(blue_alliance)

            matches_added += 1
            print("Added match {0} ({1}/{2}/{3} vs {4}/{5}/{6})".format(match['key'],
                                                                        red_alliance.teams.all()[0].team_number,
                                                                        red_alliance.teams.all()[1].team_number,
                                                                        red_alliance.teams.all()[2].team_number,
                                                                        blue_alliance.teams.all()[0].team_number,
                                                                        blue_alliance.teams.all()[1].team_number,
                                                                        blue_alliance.teams.all()[2].team_number))


class Command(BaseCommand):
    help = "Adds matches to the database"

    def add_arguments(self, parser):
        parser.add_argument('--event', dest='event', default='', type=str)

    def handle(self, *args, **options):
        event = options['event']
        add_matches_from_event(event)
