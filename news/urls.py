from django.urls import path

from .views import PostListView, PostDeleteView

app_name = 'news'
urlpatterns = [    
    path('', PostListView.as_view(), name='news'),
    path('<int:pk>', PostDeleteView.as_view(), name='new'),
]