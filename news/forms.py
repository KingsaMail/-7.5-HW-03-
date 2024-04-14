from django import forms

from .models import Post

class PostArticleCreate(forms.ModelForm):
    
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     # project = Project.objects.get(slug=self.kwargs['project_slug'])
    #     # form.instance.project = project
    #     return super(self).form_valid(form) #ResponseCreate, перед self
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['field'].initial = 'z'
    
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']
        