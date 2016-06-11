from time import clock

from TBAW.TBAW_requester import get_list_of_matches_json, get_event_json
from TBAW.models import Match, Alliance, Event
from django.core.management.base import BaseCommand
from util.check import match_exists, alliance_exists, event_has_f3_match
from util.getters import get_team, get_event, get_alliance, get_instance_scoring_model
from .addelo import handle_match_elo

matches_created = 0
matches_skipped = 0


def add_all_matches():
    events = Event.objects.exclude(key__in=['2016cmp', '2016cc']).order_by('end_date')
    for event in events:
        add_matches_from_event(event.key)

    # force CMP to be the last event processed during the championship weekend
    # ...except offseasons
    add_matches_from_event('2016cmp')
    add_matches_from_event('2016cc')


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

            if match['score_breakdown'] is None:
                print("Skipping match {0} from event {1} (scores not found)".format(match['key'], event_key))
                matches_skipped += 1
                continue

            if match['comp_level'] in ['ef', 'qf', 'sf', 'f']:
                event_json = None
                if not alliance_exists(red_teams):
                    event_json = get_event_json(event_key)
                    # print(event_json['alliances'])
                    red_alliance = Alliance.objects.create()
                    red_alliance.color = 'Red'
                    for data_seg in event_json['alliances']:
                        if red_teams[0].key in data_seg['picks']:
                            try:
                                red_alliance.seed = int(data_seg['name'][-1:])
                            except ValueError:
                                print("Can't retrieve a seed from {}".format(data_seg['name']))

                    red_alliance.save()
                    get_event(event_key).alliances.add(red_alliance)
                    for x in red_teams:
                        red_alliance.teams.add(x)
                else:
                    red_alliance = get_alliance(red_teams)
                if not alliance_exists(blue_teams):
                    if event_json is None:
                        event_json = get_event_json(event_key)
                    blue_alliance = Alliance.objects.create()
                    blue_alliance.color = 'Blue'
                    for data_seg in event_json['alliances']:
                        if blue_teams[0].key in data_seg['picks']:
                            try:
                                blue_alliance.seed = int(data_seg['name'][-1:])
                            except ValueError:
                                print("Can't retrieve a seed from {}".format(data_seg['name']))
                    blue_alliance.save()
                    get_event(event_key).alliances.add(blue_alliance)
                    for x in blue_teams:
                        blue_alliance.teams.add(x)
                else:
                    blue_alliance = get_alliance(blue_teams)
            else:
                red_alliance = Alliance.objects.create()
                red_alliance.color = 'Red'
                red_alliance.save()
                blue_alliance = Alliance.objects.create()
                blue_alliance.color = 'Blue'
                blue_alliance.save()

                for x, y in zip(red_teams, blue_teams):
                    red_alliance.teams.add(x)
                    blue_alliance.teams.add(y)

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
                                             event=get_event(event_key), winner=winner,
                                             scoring_model=parse_score_breakdown(match['key'][:4],
                                                                                 match['score_breakdown']))
            match_obj.save()
            match_obj.alliances.add(red_alliance)
            match_obj.alliances.add(blue_alliance)

            handle_match_elo(match_obj)

            matches_created += 1
            print("({7}) Added match {0} ({1}/{2}/{3} vs {4}/{5}/{6})".format(match['key'],
                                                                              red_alliance.teams.all()[0].team_number,
                                                                              red_alliance.teams.all()[1].team_number,
                                                                              red_alliance.teams.all()[2].team_number,
                                                                              blue_alliance.teams.all()[0].team_number,
                                                                              blue_alliance.teams.all()[1].team_number,
                                                                              blue_alliance.teams.all()[2].team_number,
                                                                              matches_created))


def parse_score_breakdown(year, score_breakdown):
    if type(year) is not int:
        year = int(year)

    model = get_instance_scoring_model(year).objects.create()
    model.setup(score_breakdown)
    model.save()
    return model


def handle_event_winners():
    matches_of_3 = Match.objects.filter(comp_level__exact='f', match_number__exact=3, winner__isnull=False)
    matches_of_2 = Match.objects.filter(
        key__in=[x.key for x in Match.objects.filter(comp_level__exact='f', match_number__exact=2,
                                                     winner__isnull=False) if not event_has_f3_match(x.event.key)])
    matches = (matches_of_2 | matches_of_3)

    for m in matches:
        print("{0} won {1}".format(m.winner, m))
        m.event.winning_alliance = m.winner
        m.event.save()


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
        handle_event_winners()
        time_end = clock()
        print("-------------")
        print("Matches created:\t\t{0}".format(matches_created))
        print("Matches skipped:\t\t{0}".format(matches_skipped))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
