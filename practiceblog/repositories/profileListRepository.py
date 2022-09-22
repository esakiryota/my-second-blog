from cmath import log
from ..models import ProfileList
import random, string
from ..aws_s3_storage import MediaStorage
import json

class ProfileListRepository :

    def insert(self, author, display_name="", introduce="", image=""):
        ob = ProfileList(author=author, display_name=display_name, introduce=introduce, image=image)
        ob.save()
        return {"display_name": display_name,"introduce": introduce, "image": image}
    
    def update(self, author, display_name="", introduce="", image=""):
        result_num = ProfileList.objects.filter(author=author)
        if len(result_num) == 0:
            return self.insert(author, display_name, introduce, image)
        result = ProfileList.objects.get(author=author)
        result.display_name = display_name
        result.introduce = introduce
        if image != "":
            result.image = image
        result.save()
        return {"display_name": result.display_name,"introduce": result.introduce, "image": result.image}
    
    def getProfileByAuthor(self, author):
        result = ProfileList.objects.filter(author=author)
        profile = list(result.values())
        return profile[0]

    def getImageByUrl(self, url):
        storage = MediaStorage()
        file_url = storage.url(url)
        return file_url
    
    def getAllProfilesForView(self):
        profiles = ProfileList.objects.select_related('author')
        result_list = []
        for profile in profiles:
            image_src = ""
            if profile.image != "":
                image_src = self.getImageByUrl(profile.image)
            dict = {"display_name": profile.display_name, "image": profile.image, "introduce": profile.introduce, "image_src": image_src, "author": {"username": profile.author.username, "id": profile.author.id, "pk": profile.author.pk}}
            result_list.append(dict)
        return result_list
