from ..models import RelationshipList
import random, string

class RelationshipListRepository :


    def insert(self, follow_id, follower_id):
        ob_follow = RelationshipList.objects.filter(follow=follow_id).filter(follower=follower_id)
        if len(ob_follow) != 0:
            return {"message": "すでにフォローしています"}
        ob = RelationshipList(follow=follow_id, follower=follower_id)
        ob.save()
        return {"follow" : follow_id, "follower" : follower_id}
    
    def delete(self, follow_id, follower_id):
        ob_follow = RelationshipList.objects.filter(follow=follow_id).filter(follower=follower_id)
        if len(ob_follow) == 0:
            return {"message": "すでに削除されています"}
        ob_follow.delete()
        return {"follow" : follow_id, "follower" : follower_id}
    
    def getRelationshipListByUserId(self, user_id):
        ob_follow = RelationshipList.objects.filter(follow=user_id)
        ob_follower = RelationshipList.objects.filter(follower=user_id)
        follower_list = []
        follow_list = []
        for value in list(ob_follower.values()):
            follower_list.append(value["follow"])
        
        for value in list(ob_follow.values()):
            follow_list.append(value["follower"])
        


        return {"follower_list": follower_list, "follow_list": follow_list}

    def getMutalFollowRelationship(self, user_id):
        relationship_list = self.getRelationshipListByUserId(user_id)
        follow_list = relationship_list["follow_list"]
        follower_list = relationship_list["follower_list"]
        mutal_follow = []
        for i in follow_list:
            if i in follower_list:
                mutal_follow.append(i)
        return mutal_follow
    
    def getRalationShipBool(self, user_id_1, user_id_2):
        relation_1 = RelationshipList.objects.filter(follow=user_id_1).filter(follower=user_id_2)
        relation_2 = RelationshipList.objects.filter(follow=user_id_2).filter(follower=user_id_1)
        relation_bool = False
        if len(relation_1) != 0 and len(relation_2) != 0:
            relation_bool = True
        return relation_bool


