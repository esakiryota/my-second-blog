from ..models import UserTokenList
import random, string


class UserTokenListRepository :

    def randomname(self, n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        return ''.join(randlst)

    def createToken(self, author):
        token = self.randomname(15)
        ob = UserTokenList(author=author, token=token)
        ob.save()
        return token

    def getUserToken(self, author):
        ob = UserTokenList.objects.filter(author=author)
        if ob.first() is None:
            token = self.createToken(author)
        else:
            user_token = ob.get()
            token = user_token.token
        return token
    
    def getTokenList(self, author):
        ob = UserTokenList.objects.exclude(author=author)
        return ob


