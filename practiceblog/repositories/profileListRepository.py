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
        print(file_url)
        # image_src = json.loads(file)
        return file_url