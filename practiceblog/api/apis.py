from django.http import JsonResponse
import json
import os


def updateRoom(request, room_name):
    data = request.body
    data_byte = (len(data)/1024)/1024
    print(data_byte)
    data = json.loads(data)
    MAX_BYTE = 10
    board_byte = (getJsonFileSize(room_name)/1024)/1024
    d = {}
    if (MAX_BYTE < data_byte):
        d["message"] = "ボードのデータ上限に達しました。保存するには、ボードの使わないデータを削除してください"
    else :
        with open(f'practiceblog/boards/{room_name}.json', "w") as f:
            json.dump(data, f)
            d['message'] = "保存しました。"
    return JsonResponse(d)

def loadRoom(request, room_name):
    json_open = open(f'practiceblog/boards/{room_name}.json', 'r')
    json_load = json.load(json_open)
    return JsonResponse({"data": json_load})

def getJsonFileSize(room_name):
    file_size = os.path.getsize(f'practiceblog/boards/{room_name}.json')
    return file_size