import json

from django.core.serializers import serialize
from django.apps import apps
import django.http as dhttp
from django.http import JsonResponse, HttpResponseBadRequest

from annoying.decorators import ajax_request

from TBAW.models import Team, Event
from util.viewutils import ajax_success, ajax_failure, require_http_methods_plus, make_querydict_from_request

PAGE_AMOUNT = 50

def error_response(request):
    return HttpResponseBadRequest(request)


def object_to_json(obj):
    return json.loads(serialize('json', [obj, ]))[0]


def object_list_to_json(obj_list):
    return json.loads(serialize('json', obj_list))


@ajax_request
def team_json(request, team_number):
    obj = Team.objects.get(team_number=team_number)
    print(obj)
    return obj


def team_list_json(request, page):
    page = int(page)
    if page < 1:
        return error_response(request)

    start_index = PAGE_AMOUNT * (page - 1)
    end_index = PAGE_AMOUNT * page
    obj = Team.objects.all()[start_index:end_index]
    return JsonResponse(object_list_to_json(obj), safe=False)


def event_json(request, event_key):
    obj = Event.objects.get(key=event_key)
    return JsonResponse(object_to_json(obj), safe=False)


def event_list_json(request, page):
    page = int(page)
    if page < 1:
        return error_response(request)

    start_index = PAGE_AMOUNT * (page - 1)
    end_index = PAGE_AMOUNT * page
    obj = Event.objects.all()[start_index:end_index]
    return JsonResponse(object_list_to_json(obj), safe=False)
