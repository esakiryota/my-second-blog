from django import forms

from .models import Post
from .models import Image
from .models import Question
from .models import Solve

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'cate', 'text', 'image')

class FindForm(forms.Form):
    find = forms.CharField(label='検索', required=False)

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('cate', 'title', 'image')

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('cate', 'title', 'image')

class SolveForm(forms.ModelForm):

    class Meta:
        model = Solve
        fields = ('cate', 'title', 'image')
