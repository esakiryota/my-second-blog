from django.http import JsonResponse
import json
import os

from practiceblog.views import json_serial
from ..repositories.userRepository import UserRepository
from ..repositories.relationshipListRepository import RelationshipListRepository
from ..models import RelationshipList
from ..repositories.userRepository import UserRepository
from ..repositories.userTokenListRepository import UserTokenListRepository


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
    if os.path.exists(f'practiceblog/boards/{room_name}.json') == False:
        with open(f'practiceblog/boards/{room_name}.json', "w") as f:
            json.dump("", f)
    json_open = open(f'practiceblog/boards/{room_name}.json', 'r')
    json_load = json.load(json_open)
    return JsonResponse({"data": json_load})

def getJsonFileSize(room_name):
    file_size = os.path.getsize(f'practiceblog/boards/{room_name}.json')
    return file_size

def getUserListBySearch(request):
    data = ""
    rps = UserRepository()


    return JsonResponse(data)

def userList(request):
    data = ""
    return JsonResponse(data)

def user_follow(request):
    # relationshipModel = RelationshipList()
    value = int(request.GET.get('follow_id'))
    user_id = request.user.pk
    rps = RelationshipListRepository()
    data = rps.insert(user_id, value) 
    return JsonResponse({"data": data})

def user_unfollow(request):
    # relationshipModel = RelationshipList()
    value = int(request.GET.get('follow_id'))
    user_id = request.user.pk
    rps = RelationshipListRepository()
    data = rps.delete(user_id, value) 
    return JsonResponse({"data": data})

def user_search(request):
    value = request.GET.get('str')
    author = request.user
    user_rps = UserRepository()
    result = user_rps.getUserListByUsername(value)
    json_serial = list(result.values())


    data = result
    return JsonResponse({"data": json_serial})

def board_search(request):
    value = request.GET.get('str')
    author = request.user
    usertoken_rps = UserTokenListRepository()
    result = usertoken_rps.getTokenListByMutalFollowAndUsername(author, value)
    return JsonResponse({"data": result})

def getUserInfo(request):
    value = request.body
    data = json.loads(value)
    usertoken_rps = UserTokenListRepository()
    user_rps = UserRepository()
    result = usertoken_rps.getUserInfoByToken(data["token"])
    user_info = user_rps.getUserById(result.pk)
    user_info["token"] = data["token"]

    return JsonResponse({"data": user_info})





# def createPage(data, num):
#     result = {}
#     for value in data:
        
#     return result