from django.http import JsonResponse
import json


def updateRoom(request, room_name):
    d = {
        'ok' : 'ok'
    }
    data = request.body
    data = json.loads(data);
    with open(f'practiceblog/boards/{room_name}.json', "w") as f:
        json.dump(data, f)
    return JsonResponse(d)

def loadRoom(request, room_name):
    json_open = open(f'practiceblog/boards/{room_name}.json', 'r')
    json_load = json.load(json_open)
    return JsonResponse({"data": json_load})