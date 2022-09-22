from django.contrib.auth import get_user_model
import random, string
from practiceblog.repositories.userTokenListRepository import UserTokenListRepository

class UserRepository :


    User = get_user_model()

    def getUserById(self, id):
        ob = self.User.objects.filter(id=id)
        user = list(ob.values())
        return user[0]

    def getUserAllList(self):
        result = self.User.objects.all()
        return result

    def getUserListByUsername(self, str):
        if str == "":
            result = self.getUserAllList()
            return result
        result = self.User.objects.filter(username__contains=str)
        return result

    def getUserAllListForView(self):
        result = self.getUserAllList()
        result_list = []
        for user in result:
            dict = {"username": user.username, "id": user.pk}
            result_list.append(dict)
        return result_list
    
    def getUserObjectById(self, id):
        ob = self.User.objects.get(id=id)
        return ob

