from django import forms

from .models import *


class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraph
        exclude = ('post', 'order', 'id')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('editor',)
