from django.contrib import admin
from .models import Post
from .models import Image
from .models import Question
from .models import Solve
from .models import Introduce
from .models import QuestionBox

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Question)
admin.site.register(Solve)
admin.site.register(Introduce)
admin.site.register(QuestionBox)
