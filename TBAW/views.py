from datetime import date

from django.db.models import F, Q
from annoying.decorators import render_to

from FRS.views import handle_404
from TBAW.models import Event, RankingModel, Team, ScoringModel, Alliance
from util.check import alliance_exists, team_exists
from util.getters import get_team, get_event, get_alliance


@render_to("TBAW/team_view.html")
def team_view(request, team_number):
    if Team.objects.filter(team_number=team_number).exists():
        team = get_team(team_number)
        events_this_year = Event.objects.prefetch_related('teams')\
            .filter(year=date.today().year, teams__team_number=team.team_number).order_by('end_date').values('key', 'year', 'name')

        return {
            'team': team,
            'events': events_this_year,
            'awards_count': team.awards_count,
            'blue_banners_count': team.blue_banners_count,
        }
    else:
        return handle_404(request)


@render_to('TBAW/event_view.html')
def event_view(request, event_key):
    if Event.objects.filter(key=event_key).exists():
        event = get_event(event_key)
        matches = event.match_set.all()

        def create_team_map(t: Team):
            return {
                'team_number': t.team_number,
                'label': str(t)
            }

        #
        # Optimizations here rely on lookup tables which may use an *excessive* amount of memory to load this page, to
        # offload this task of caching to the Django ORM, we may be able to change queries to use select_related and
        # prefetch_related.
        #

        # Assembling Alliances Lookup Table
        alliance_ids = [m.red_alliance_id for m in matches] + [m.blue_alliance_id for m in matches]
        alliances_by_id = {a.id: a for a in Alliance.objects.prefetch_related('teams').filter(id__in=alliance_ids)}
        alliances_by_match = {m: (alliances_by_id[m.red_alliance_id], alliances_by_id[m.blue_alliance_id])
                              for m in matches}

        # Dictionary matching Match instances to list of pairs of the form (team_number, string representation)
        matches_to_alliances = {
            m: (tuple(create_team_map(t) for t in alliances_by_match[m][0].teams.all()),
                tuple(create_team_map(t) for t in alliances_by_match[m][1].teams.all()))
                for m in matches}

        # Assembling Scoring Model Lookup Table
        scoring_model_ids = [m.scoring_model_id for m in matches]
        models = {m.id: m for m in ScoringModel.objects.filter(Q(id__in=scoring_model_ids)).all()}
        matches_to_scoring_models = {m: models[m.scoring_model_id] for m in matches}

        # Assemble RankingModel Lookup Table
        ranking_models = RankingModel.objects.select_related('event').filter(event__key=event_key).annotate(team_number=F('team__team_number')).all()
        ranking_models = {x.team_number: x for x in ranking_models}

        return {
            'event': event,
            'ranking_models': ranking_models,
            'matches': matches,
            'match_alliances': matches_to_alliances,
            'match_scorings': matches_to_scoring_models
        }
    else:
        return handle_404(request)


def alliance_view(request, team1: str, team2: str, team3: str):
    team1 = int(team1)
    team2 = int(team2)
    team3 = int(team3)

    if team_exists(team1):
        team1 = get_team(team1)
    if team_exists(team2):
        team2 = get_team(team2)
    if team_exists(team3):
        team3 = get_team(team3)

    if alliance_exists(team1, team2, team3):
        return alliance_exists_view(request, get_alliance(team1, team2, team3))
    else:
        return alliance_does_not_exist_view(request, [team1, team2, team3])


def alliance_view_alliance_obj(request, alliance_obj):
    teams = alliance_obj.teams.all()
    return alliance_view(request, teams[0].team_number, teams[1].team_number, teams[2].team_number)


@render_to('TBAW/alliance_exists.html')
def alliance_exists_view(request, alliance):
    events = Event.objects.filter(allianceappearance__alliance=alliance).order_by('-end_date')
    # wins = alliance.get_wins()
    # losses = alliance.get_losses()
    # ties = alliance.get_ties()

    return {
        'alliance': alliance,
        'events': events,
    }


@render_to('TBAW/alliance_does_not_exist.html')
def alliance_does_not_exist_view(request, teams):
    return {
        'teams': teams
    }
