from typing import Iterable, List, Optional
from time import clock

import collections

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F, Q, ExpressionWrapper, FloatField, Count

from TBAW.models import Match, Alliance, Event, AllianceAppearance, RankingModel, Team, ScoringModel
from TBAW.requester import get_list_of_matches_json_async, get_event_json_async
from TBAW.resource_getter import AsyncRequester
from util.check import alliance_exists
from util.getters import get_alliance, get_instance_scoring_model, get_teams

matches_created = 0
matches_skipped = 0
event_matches = 0

YEAR_TO_POINT_STR = {
    2016: 'Points',
    2015: '_points'
}

file_requester = AsyncRequester(use_threads=False)
TeamScoreOverview2016 = collections.namedtuple('TeamScoreOverview2016', ['alliance', 'total', 'foul', 'breach', 'auto'])


def add_all_matches(*years: Iterable[int]) -> None:
    years = [*years]
    events = Event.objects.prefetch_related('alliances').filter(year__in=years).order_by('end_date').all()
    for event in events:
        add_matches_from_event(event)


def add_matches_from_event(event: Event) -> None:
    get_list_of_matches_json_async(file_requester, event.key, _add_matches_from_event_async, event)


def _add_matches_from_event_async(event: Event, matches_json: List[dict]) -> None:
    global matches_created, matches_skipped, event_matches
    matches = matches_json
    current_seed = 1

    event_json_future = get_event_json_async(file_requester, event.key)

    print("Adding matches from event {0}...".format(event.key))
    all_matches_for_event = {k for k in Match.objects.filter(event_id=event.id).values_list('key', flat=True).all()}
    alliance_to_appearance = {ap.alliance_id: ap for ap in AllianceAppearance.objects.filter(event_id=event.id).all()}
    team_to_rankingmodel = {rm.team_id: rm for rm in RankingModel.objects.filter(event_id=event.id).all()}

    def get_or_create_appearance(alliance: Alliance, seed: int):
        if alliance.id not in alliance_to_appearance:
            appearance = AllianceAppearance.objects.create(alliance_id=alliance.id, event_id=event.id,
                                                                       seed=seed)
            alliance.allianceappearance_set.add(appearance)
        else:
            appearance = AllianceAppearance.objects.get(alliance_id=alliance.id, event_id=event.id)
            appearance.seed = seed
            appearance.save()
        return appearance

    def get_or_create_alliance(team_one: Team, team_two: Team, team_three: Team):
        if not alliance_exists(team_one, team_two, team_three):
            alliance = Alliance.objects.create()

            with transaction.atomic():
                for x in [team_one, team_two, team_three]:
                    red_alliance.teams.add(x)
        else:
            alliance = get_alliance(team_one, team_two, team_three)

        return alliance

    def determine_seed_offset(evt_json: dict, team: Team):
        seed_offset = 0
        for data_seg in evt_json['alliances']:
            if team.key in data_seg['picks']:
                seed_offset += 1
        return seed_offset

    for match in matches:
        match_year = int(match['key'][:4])

        if match['key'] in all_matches_for_event:
            matches_skipped += 1
            print("({1}) Already added {0}".format(match['key'], matches_skipped))
        else:
            score_breakdwown_available = not (match['score_breakdown'] is None and match_year >= 2015)
            alliances_scores_available = not (match['alliances']['blue']['score'] == match['alliances']['red']['score'] == -1)

            if not score_breakdwown_available or not alliances_scores_available:
                print("Skipping match {0} from event {1} (scores not found)".format(match['key'], event.key))
                matches_skipped += 1
                continue

            red_ids = {int(team_id[3:]) for team_id in match['alliances']['red']['teams']}
            blue_ids = {int(team_id[3:]) for team_id in match['alliances']['blue']['teams']}
            all_teams = get_teams(*(red_ids | blue_ids))

            red_teams = [team for team in all_teams if team.id in red_ids]
            blue_teams = [team for team in all_teams if team.id in blue_ids]
            red_seed = None
            blue_seed = None

            red_alliance = get_or_create_alliance(*red_teams)
            blue_alliance = get_or_create_alliance(*blue_teams)

            red_total_points = match['alliances']['red']['score']
            blue_total_points = match['alliances']['blue']['score']

            if event.year in YEAR_TO_POINT_STR:
                pt_str = YEAR_TO_POINT_STR[event.year]

                red_score_breakdown = match['score_breakdown']['red']
                blue_score_breakdown = match['score_breakdown']['blue']

                red_total_points = red_score_breakdown.get('total{0}'.format(pt_str), red_total_points)
                blue_total_points = blue_score_breakdown.get('total{0}'.format(pt_str), blue_total_points)
                red_foul_points = red_score_breakdown.get('foul{0}'.format(pt_str), 0)
                blue_foul_points = blue_score_breakdown.get('foul{0}'.format(pt_str), 0)

            if red_total_points < blue_total_points:
                winner = blue_alliance
            elif red_total_points > blue_total_points:
                winner = red_alliance
            elif match['comp_level'] in ['ef', 'qf', 'sf', 'f']:
                if event.year == 2016:
                    red_breach_capture_points = red_score_breakdown['breach{0}'.format(pt_str)] + red_score_breakdown['capture{0}'.format(pt_str)]
                    blue_breach_capture_points = blue_score_breakdown['breach{0}'.format(pt_str)] + blue_score_breakdown['capture{0}'.format(pt_str)]
                    red_auto_points = red_score_breakdown['auto{0}'.format(pt_str)]
                    blue_auto_points = blue_score_breakdown['auto{0}'.format(pt_str)]

                    red_overview = TeamScoreOverview2016(red_alliance, red_total_points, red_foul_points,
                                                         red_breach_capture_points, red_auto_points)
                    blue_overview = TeamScoreOverview2016(blue_alliance, blue_total_points, blue_foul_points,
                                                          blue_breach_capture_points, blue_auto_points)

                    winner = determine_elims_winner2016(red_overview, blue_overview)
                elif event.year == 2015:
                    winner = None
                elif event.year in [2010, 2011, 2012, 2013, 2014]:
                    winner = None  # Elims were replayed in case of a tie
            else:
                winner = None

            if winner == blue_alliance:
                loser = red_alliance
            elif winner == red_alliance:
                loser = blue_alliance
            else:
                loser = None

            with transaction.atomic():
                red_alliance.save()
                blue_alliance.save()
                event.alliances.add(red_alliance)
                event.alliances.add(blue_alliance)

            parse_key = match_year
            parse_old_kwargs = {'red_score': red_total_points, 'blue_score': blue_total_points}
            parse_new_args = (parse_key, match['score_breakdown'])

            old_parse = parse_old_matches
            new_parse = parse_score_breakdown

            sm = new_parse(*parse_new_args) if match['score_breakdown'] else old_parse(parse_key, **parse_old_kwargs)

            match_obj = Match.objects.create (
                key=match['key'], comp_level=match['comp_level'], set_number=match['set_number'],
                match_number=match['match_number'], event=event, winner=winner, scoring_model=sm,
                blue_alliance=blue_alliance, red_alliance=red_alliance
            )

            match_obj.alliances.set([red_alliance, blue_alliance])

            event_json = event_json_future()
            if match['comp_level'] in ['ef', 'qf', 'sf', 'f']:
                current_seed += determine_seed_offset(event_json, red_teams[0])
                red_seed = current_seed - 1
                current_seed += determine_seed_offset(event_json, blue_teams[0])
                blue_seed = current_seed - 1

            with transaction.atomic():
                red_appearance = get_or_create_appearance(red_alliance, red_seed)
                blue_appearance = get_or_create_appearance(blue_alliance, blue_seed)

            alliance_to_appearance[red_alliance.id] = red_appearance
            alliance_to_appearance[blue_alliance.id] = blue_appearance

            if winner is None:
                with transaction.atomic():
                    for bt, rt in zip(blue_alliance.teams.all(), red_alliance.teams.all()):
                        bt_rm = RankingModel.objects.get(team=bt, event=event)
                        bt_rm.total_ties += 1; bt.match_ties_count += 1

                        rt_rm = RankingModel.objects.get(team=rt, event=event)
                        rt_rm.total_ties += 1; rt.match_ties_count += 1

                        if match['comp_level'] == 'qm':
                            bt_rm.qual_ties += 1; rt_rm.qual_ties += 1

                        bt_rm.save(); rt_rm.save()
                        bt.save();  rt.save()
            else:
                with transaction.atomic():
                    for winning_team, losing_team in zip(winner.teams.all(), loser.teams.all()):
                        winner_rm = team_to_rankingmodel[winning_team.id]
                        winner_rm.total_wins += 1; winning_team.match_wins_count += 1

                        loser_rm = team_to_rankingmodel[losing_team.id]
                        loser_rm.total_losses += 1; losing_team.match_losses_count += 1

                        if match['comp_level'] == 'qm':
                            winner_rm.qual_wins += 1; loser_rm.qual_losses += 1

                        winner_rm.save(); loser_rm.save()
                        winning_team.save(); losing_team.save()

            matches_created += 1
            event_matches += 1

    print("\tSuccessfully added {0} matches from event".format(event_matches))
    event_matches = 0


def determine_elims_winner2016(red: TeamScoreOverview2016, blue: TeamScoreOverview2016) -> Optional[Alliance]:
    red_alliance = red.alliance
    blue_alliance = blue.alliance

    if red.total + red.foul > blue.total + blue.foul:
        winner = red_alliance
    elif red.total + red.foul < blue.total + blue.foul:
        winner = blue_alliance
    elif red.breach > blue.breach:
        winner = red_alliance
    elif red.breach < blue.breach:
        winner = blue_alliance
    elif red.auto > blue.auto:
        winner = red_alliance
    elif red.auto < blue.auto:
        winner = blue_alliance
    else:
        winner = None

    return winner


def parse_score_breakdown(year: int, score_breakdown: dict) -> ScoringModel:
    model = get_instance_scoring_model(year).objects.create()
    try:
        model.setup(score_breakdown)
    except KeyError:
        pass  # fail silently for now
    model.save()
    return model


def parse_old_matches(year: int, red_score: int, blue_score: int) -> ScoringModel:
    model = get_instance_scoring_model(year).objects.create()
    model.red_total_score = red_score
    model.blue_total_score = blue_score
    model.save()
    return model


def handle_event_winners() -> None:
    print('Handling event winners...', flush=True)

    match_of_3_or_2 = Q(comp_level='f') & (Q(match_number=3) | Q(match_number=2)) & Q(winner__isnull=False)

    # Find all 'f' level matches with match_number == 2 or 3
    matches = Match.objects.filter(match_of_3_or_2)

    # Find all event ids that occur more than once
    dupes = matches.values('event').annotate(Count('id')).filter(id__count__gt=1).values('event')
    dupes = {x['event'] for x in dupes}  # values returns a list of dicts

    # Perform update in aggregate, in a single transaction
    with transaction.atomic():
        for m in matches:
            # Do not update matches that were picked up in the match_number=2 query
            # but went on to a 3rd match. That event_id would then appear twice.
            if m.match_number == '2' and m.event_id in dupes:
                dupes.remove(m.event_id)
                continue

            m.event.winning_alliance = m.winner
            m.event.save()

            m.winner.teams.all().update(event_wins_count=F('event_wins_count') + 1)

    # Update event winrates based on event wins and events attended
    Team.objects.exclude(event_attended_count=0) \
        .update(event_winrate=(F('event_wins_count') * 1.0 / F('event_attended_count')))

    # Update match winrate based on total matches played and total matches won
    Team.objects.exclude(match_losses_count=0, match_wins_count=0) \
        .annotate(played=F('match_wins_count') + F('match_losses_count') + F('match_ties_count')) \
        .update(match_winrate=ExpressionWrapper(F('match_wins_count') * 1.0 / F('played'), output_field=FloatField()))


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
                for yr in [2015, 2016]:  # SUPPORTED_YEARS:
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
