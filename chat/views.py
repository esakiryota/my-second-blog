from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

def updateRoom(request, room_name):
    d = {
        'ok' : 'ok'
    }
    print(d)
    return JsonResponse(d)

    