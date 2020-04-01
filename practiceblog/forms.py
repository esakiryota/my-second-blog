from django import forms

from .models import Post
from .models import ImageBox
from .models import Question
from .models import Solve
from .models import QuestionBox
from .models import QuestionSolve

from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)
from django.contrib.auth import get_user_model

User = get_user_model()

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'cate', 'text', 'image')

class FindForm(forms.Form):
    find = forms.CharField(label='検索', required=False)

class ImageBoxForm(forms.ModelForm):

    class Meta:
        model = ImageBox
        fields = ('cate', 'title', 'image')

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('cate', 'title', 'image', 'time')

class SolveForm(forms.ModelForm):

    class Meta:
        model = Solve
        fields = ('cate', 'title', 'image')

class QuestionBoxForm(forms.ModelForm):

    class Meta:
        model = QuestionBox
        fields = ('cate', 'title', 'image', 'comment', 'bool')

class QuestionSolveForm(forms.ModelForm):

    class Meta:
        model = QuestionSolve
        fields = ('cate', 'title', 'image', 'comment')

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'groups')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=True).delete()
        return email
