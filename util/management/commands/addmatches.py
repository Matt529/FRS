from time import clock

from django.core.management.base import BaseCommand
from django.db.models import F, ExpressionWrapper, FloatField

from FRS.settings import SUPPORTED_YEARS
from TBAW.models import Match, Alliance, Event, AllianceAppearance, RankingModel, Team, ScoringModel
from TBAW.requester import get_list_of_matches_json, get_event_json
from util.check import match_exists, alliance_exists, alliance_appearance_exists
from util.getters import get_team, get_event, get_alliance, get_instance_scoring_model

matches_created = 0
matches_skipped = 0
event_matches = 0


def add_all_matches(year: int) -> None:
    events = Event.objects.filter(year=year).order_by('end_date')
    for event in events:
        add_matches_from_event(event.key)


def add_matches_from_event(event_key: str) -> None:
    global matches_created, matches_skipped, event_matches
    matches = get_list_of_matches_json(event_key)
    current_seed = 1
    print("Adding matches from event {0}...".format(event_key))
    for match in matches:
        if match_exists(event_key, match['key']):
            matches_skipped += 1
            print("({1}) Already added {0}".format(match['key'], matches_skipped))
        else:
            red_teams = [get_team(int(x[3:])) for x in match['alliances']['red']['teams']]
            blue_teams = [get_team(int(x[3:])) for x in match['alliances']['blue']['teams']]
            red_seed = None
            blue_seed = None

            if match['score_breakdown'] is None or (
                        match['alliances']['blue']['score'] == -1 and match['alliances']['red']['score'] == -1):
                print("Skipping match {0} from event {1} (scores not found)".format(match['key'], event_key))
                matches_skipped += 1
                continue

            event_json = get_event_json(event_key)
            event = get_event(event_key)
            if match['comp_level'] in ['ef', 'qf', 'sf', 'f']:
                if not alliance_exists(red_teams[0], red_teams[1], red_teams[2]):
                    red_alliance = Alliance.objects.create()
                    event.alliances.add(red_alliance)
                    for x in red_teams:
                        red_alliance.teams.add(x)
                else:
                    red_alliance = get_alliance(red_teams[0], red_teams[1], red_teams[2])

                for data_seg in event_json['alliances']:
                    if red_teams[0].key in data_seg['picks']:
                        red_seed = current_seed
                        current_seed += 1

                if not alliance_exists(blue_teams[0], blue_teams[1], blue_teams[2]):
                    blue_alliance = Alliance.objects.create()
                    event.alliances.add(blue_alliance)
                    for x in blue_teams:
                        blue_alliance.teams.add(x)
                else:
                    blue_alliance = get_alliance(blue_teams[0], blue_teams[1], blue_teams[2])

                for data_seg in event_json['alliances']:
                    if blue_teams[0].key in data_seg['picks']:
                        blue_seed = current_seed
                        current_seed += 1
            else:
                red_alliance = Alliance.objects.create()
                blue_alliance = Alliance.objects.create()

                for x, y in zip(red_teams, blue_teams):
                    red_alliance.teams.add(x)
                    blue_alliance.teams.add(y)

            if event.year in [2015, 2016]:
                if event.year == 2016:
                    pt_str = 'Points'
                elif event.year == 2015:
                    pt_str = '_points'

                red_score_breakdown = match['score_breakdown']['red']
                blue_score_breakdown = match['score_breakdown']['blue']

                try:
                    red_total_points = red_score_breakdown['total{0}'.format(pt_str)]
                    blue_total_points = blue_score_breakdown['total{0}'.format(pt_str)]
                    red_foul_points = red_score_breakdown['foul{0}'.format(pt_str)]
                    blue_foul_points = blue_score_breakdown['foul{0}'.format(pt_str)]
                except KeyError:
                    red_total_points = match['alliances']['red']['score']
                    blue_total_points = match['alliances']['blue']['score']
                    red_foul_points = 0
                    blue_foul_points = 0
            else:
                red_total_points = match['alliances']['red']['score']
                blue_total_points = match['alliances']['blue']['score']

            if red_total_points < blue_total_points:
                winner = blue_alliance
            elif red_total_points > blue_total_points:
                winner = red_alliance
            elif match['comp_level'] in ['ef', 'qf', 'sf', 'f'] and event.year == 2016:
                red_breach_capture_points = red_score_breakdown['breach{0}'.format(pt_str)] + red_score_breakdown[
                    'capture{0}'.format(pt_str)]
                blue_breach_capture_points = blue_score_breakdown['breach{0}'.format(pt_str)] + blue_score_breakdown[
                    'capture{0}'.format(pt_str)]
                red_auto_points = red_score_breakdown['auto{0}'.format(pt_str)]
                blue_auto_points = blue_score_breakdown['auto{0}'.format(pt_str)]

                if red_total_points + red_foul_points > blue_total_points + blue_foul_points:
                    winner = red_alliance
                elif red_total_points + red_foul_points < blue_total_points + blue_foul_points:
                    winner = blue_alliance
                elif red_breach_capture_points > blue_breach_capture_points:
                    winner = red_alliance
                elif blue_breach_capture_points > red_breach_capture_points:
                    winner = blue_alliance
                elif red_auto_points > blue_auto_points:
                    winner = red_alliance
                elif blue_auto_points > red_auto_points:
                    winner = blue_alliance
                else:
                    winner = None
            else:
                winner = None

            if winner == blue_alliance:
                loser = red_alliance
            elif winner == red_alliance:
                loser = blue_alliance
            else:
                loser = None

            red_alliance.save()
            blue_alliance.save()
            match_obj = Match.objects.create(key=match['key'], comp_level=match['comp_level'],
                                             set_number=match['set_number'], match_number=match['match_number'],
                                             event=event, winner=winner,
                                             scoring_model=parse_score_breakdown(int(match['key'][:4]),
                                                                                 match['score_breakdown']),
                                             blue_alliance=blue_alliance, red_alliance=red_alliance)
            match_obj.alliances.set([red_alliance, blue_alliance])

            if not alliance_appearance_exists(red_alliance, event):
                red_appearance = AllianceAppearance.objects.create(alliance=red_alliance, event=event,
                                                                   seed=red_seed)
                red_alliance.allianceappearance_set.add(red_appearance)
            else:
                red_appearance = AllianceAppearance.objects.get(alliance=red_alliance, event=event)
                red_appearance.seed = red_seed
                red_appearance.save()

            if not alliance_appearance_exists(blue_alliance, event):
                blue_appearance = AllianceAppearance.objects.create(alliance=blue_alliance, event=event,
                                                                    seed=blue_seed)
                blue_alliance.allianceappearance_set.add(blue_appearance)
            else:
                blue_appearance = AllianceAppearance.objects.get(alliance=blue_alliance, event=event)
                blue_appearance.seed = blue_seed
                blue_appearance.save()

            if winner is None:
                for bt, rt in zip(blue_alliance.teams.all(), red_alliance.teams.all()):
                    bt_rm = RankingModel.objects.get(team=bt, event=event)
                    bt_rm.total_ties += 1
                    bt.match_ties_count += 1

                    rt_rm = RankingModel.objects.get(team=rt, event=event)
                    rt_rm.total_ties += 1
                    rt.match_ties_count += 1

                    if match['comp_level'] == 'qm':
                        bt_rm.qual_ties += 1
                        rt_rm.qual_ties += 1

                    bt_rm.save()
                    rt_rm.save()
            else:
                for winning_team, losing_team in zip(winner.teams.all(), loser.teams.all()):
                    winner_rm = RankingModel.objects.get(team=winning_team, event=event)
                    winner_rm.total_wins += 1
                    winning_team.match_wins_count += 1

                    loser_rm = RankingModel.objects.get(team=losing_team, event=event)
                    loser_rm.total_losses += 1
                    losing_team.match_losses_count += 1

                    if match['comp_level'] == 'qm':
                        winner_rm.qual_wins += 1
                        loser_rm.qual_losses += 1

                    winner_rm.save()
                    loser_rm.save()

            Team.objects.bulk_update(blue_alliance.teams.all() | red_alliance.teams.all(),
                                     update_fields=['match_wins_count', 'match_losses_count', 'match_ties_count'])
            matches_created += 1
            event_matches += 1

    print("\tSuccessfully added {0} matches from event".format(event_matches))
    event_matches = 0


def parse_score_breakdown(year: int, score_breakdown: dict) -> ScoringModel:
    model = get_instance_scoring_model(year).objects.create()
    try:
        model.setup(score_breakdown)
    except KeyError:
        pass  # fail silently for now
    model.save()
    return model


def handle_event_winners() -> None:
    matches_of_3 = Match.objects.filter(comp_level__exact='f', match_number__exact=3, winner__isnull=False)
    matches_of_2 = Match.objects.filter(
        key__in=[x.key for x in Match.objects.filter(comp_level__exact='f', match_number__exact=2,
                                                     winner__isnull=False) if not x.event.has_f3_match()])
    matches = (matches_of_2 | matches_of_3)

    for m in matches:
        m.event.winning_alliance = m.winner
        m.event.save()

    year = matches_of_2.first().event.year
    Team.objects.filter(alliance__winning_alliance__year=year).update(event_wins_count=F('event_wins_count') + 1)
    Team.objects.filter(event__year=year).update(event_attended_count=F('event_attended_count') + 1)
    Team.objects.exclude(event_attended_count=0).annotate(
        wr=ExpressionWrapper(F('event_wins_count') * 1.0 / F('event_attended_count'), output_field=FloatField())
    ).update(event_winrate=F('wr'))


class Command(BaseCommand):
    help = "Adds matches to the database"

    def add_arguments(self, parser):
        parser.add_argument('--event', dest='event', default='', type=str)
        parser.add_argument('--year', dest='year', default=0, type=int)

    def handle(self, *args, **options):
        event = options['event']
        year = options['year']
        time_start = clock()
        if event is not '':
            add_matches_from_event(event)
        else:
            if year == 0:
                for yr in SUPPORTED_YEARS:
                    add_all_matches(yr)
            else:
                add_all_matches(year)
        handle_event_winners()
        time_end = clock()
        print("-------------")
        print("Matches created:\t\t{0}".format(matches_created))
        print("Matches skipped:\t\t{0}".format(matches_skipped))
        print("Ran in {0} seconds.".format((time_end - time_start).__round__(3)))
        print("-------------")
