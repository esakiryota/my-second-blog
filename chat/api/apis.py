from django.http import HttpResponse
from django.http import JsonResponse
from django.http import QueryDict
import json


def updateRoom(request, room_name):
    d = {
        'ok' : 'ok'
    }
    data = request.body
    data = json.loads(data);
    with open(f'chat/board/{room_name}.json', "w") as f:
        json.dump(data, f)
    return JsonResponse(d)

def loadRoom(request, room_name):
    json_open = open(f'chat/board/{room_name}.json', 'r')
    json_load = json.load(json_open)
    print(json_load)
    return JsonResponse({"data": json_load})