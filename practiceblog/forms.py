from django import forms

from .models import Post
from .models import Image

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
