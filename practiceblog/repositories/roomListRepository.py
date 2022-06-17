from ..models import RoomList
import random, string

class RoomListRepository :

    def insert(self, data):
        url_token = self.randomname(15)
        ob = RoomList(room_name=data["room_name"], password=data["password"], url_token=url_token)
        ob.save()
        return {"room_name" : data["room_name"], "password" : data["password"], "url_token" : url_token}

    def randomname(self, n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        return ''.join(randlst)