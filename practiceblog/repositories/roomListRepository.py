from ..models import RoomList
import random, string

class RoomListRepository :

    def insert(self, data):
        url_token = self.randomname(15)
        ob = RoomList(room_name=data["room_name"], password=data["password"], url_token=url_token, participants=0)
        ob.save()
        return {"room_name" : data["room_name"], "password" : data["password"], "url_token" : url_token}
    
    def addParticipants(self, name):
        ob = RoomList.objects.filter(url_token=name).get()
        now_participants = ob.participants
        new_participants = now_participants + 1
        ob.participants = new_participants
        ob.save()
        return new_participants
    
    def removeParticipants(self, name):
        ob = RoomList.objects.filter(url_token=name).get()
        now_participants = ob.participants
        new_participants = now_participants - 1
        ob.participants = new_participants
        ob.save()
        return new_participants

    def getNowParticipants(self, name):
        ob = RoomList.objects.filter(url_token=name).get()
        return ob.participants

    def randomname(self, n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        return ''.join(randlst)