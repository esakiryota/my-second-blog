from ..models import UserTokenList
import random, string
from .relationshipListRepository import RelationshipListRepository



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
    
    def getTokenListByMutalFollow(self, author):
        token_list = self.getTokenList(author)
        token_list_values = list(token_list.values())
        relation_rps = RelationshipListRepository()
        mutal_follow = relation_rps.getMutalFollowRelationship(author.pk)
        result = []
        for token in token_list:
            if token.author.pk in mutal_follow:
                data = {}
                data["username"] = token.author.username
                data["token"] = token.token
                result.append(data)
        return result
    
    def getTokenListByMutalFollowAndUsername(self, author, str):
        token_list = self.getTokenListByMutalFollow(author)
        if str == "":
            return token_list
        result = []
        for token in token_list:
            if str in token["username"]:
                result.append(token)
        return result

    def getUserInfoByToken(self, token):
        result = UserTokenList.objects.filter(token=token)
        return result.get().author





