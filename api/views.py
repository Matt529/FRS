import json

from TBAW.models import Team, Event
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponseBadRequest

PAGE_AMOUNT = 50


def error_response(request):
    return HttpResponseBadRequest(request)


def object_to_json(obj):
    return json.loads(serialize('json', [obj, ]))[0]


def object_list_to_json(obj_list):
    return json.loads(serialize('json', obj_list))


def team_json(request, team_number):
    obj = Team.objects.get(team_number=team_number)
    return JsonResponse(object_to_json(obj), safe=False)


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
