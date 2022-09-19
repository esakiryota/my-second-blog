from django.contrib import admin
from .models import Post
from .models import ImageBox
from .models import Question
from .models import Solve
from .models import Introduce
from .models import QuestionBox
from .models import QuestionSolve
from .models import TeacherStudent
from .models import RoomList
from .models import UserTokenList
from .models import RelationshipList
from .models import ProfileList

admin.site.register(Post)
admin.site.register(ImageBox)
admin.site.register(Question)
admin.site.register(Solve)
admin.site.register(Introduce)
admin.site.register(QuestionBox)
admin.site.register(QuestionSolve)
admin.site.register(TeacherStudent)
admin.site.register(RoomList)
admin.site.register(UserTokenList)
admin.site.register(RelationshipList)
admin.site.register(ProfileList)