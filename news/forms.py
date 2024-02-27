from django import forms

from .models import Post

class PostArticleCreate(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories', 'user']
        

