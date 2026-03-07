from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['blog', 'title', 'text']
        labels = {
            'blog': 'Blog',
            'title': 'Title',
            'text': 'Post text',
        }