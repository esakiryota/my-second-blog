from django.contrib import admin
from .models import Post
from .models import ImageBox
from .models import Question
from .models import Solve
from .models import Introduce
from .models import QuestionBox
from .models import QuestionSolve
from .models import TeacherStudent

admin.site.register(Post)
admin.site.register(ImageBox)
admin.site.register(Question)
admin.site.register(Solve)
admin.site.register(Introduce)
admin.site.register(QuestionBox)
admin.site.register(QuestionSolve)
admin.site.register(TeacherStudent)
