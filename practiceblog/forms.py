from django import forms

from .models import Post
from .models import ImageBox
from .models import Question
from .models import Solve
from .models import QuestionBox
from .models import QuestionSolve
from .models import TeacherStudent
from .models import Solve

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
        fields = ('image', )

class QuestionForm(forms.ModelForm):
    find = forms.CharField(label='検索', required=False)
    class Meta:
        model = Question
        fields = ('cate', 'title', 'image', 'time', 'grade', 'new_old', 'indi_pub', 'limited_time')

class SolveForm(forms.ModelForm):

    class Meta:
        model = Solve
        fields = ('image', 'score')

class QuestionBoxForm(forms.ModelForm):

    class Meta:
        model = QuestionBox
        fields = ('cate', 'title', 'image', 'comment', 'bool')

class QuestionSolveForm(forms.ModelForm):

    class Meta:
        model = QuestionSolve
        fields = ('title', 'image', 'comment', 'cate')

CATEGORIES = (
    ('', ''),
    ('英語', '英語'),
    ('数学', '数学'),
)

class SolveForm(forms.Form):
    cate = forms.ChoiceField(label='カテゴリ', choices=CATEGORIES, required=False)
    title = forms.CharField(label='タイトル', max_length=64, required=False)

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     User.objects.filter(email=email, is_active=True).delete()
    #     return email
    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("メールアドレスを入力して下さい")
        return cleaned_data

class TeacherStudentForm(forms.ModelForm):
    class Meta:
        model = TeacherStudent
        fields = ('user_teacher', 'user_student', 'teacher_student')

