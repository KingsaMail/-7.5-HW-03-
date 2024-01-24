from django.urls import path

from .views import (
    PostListView, PostDetailView, PostListFilter,
    ArtCreate, ArtEdit, ArtDelete,
    NewCreate, NewEdit, NewDelete
)

app_name = 'news'
urlpatterns = [    
    path('', PostListView.as_view(), name='news'),
    path('<int:pk>/', PostDetailView.as_view(), name='new'),
    path('search/', PostListFilter.as_view(), name='search'),
    # статьи
    path('articles/create/', ArtCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', ArtEdit.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', ArtDelete.as_view(), name='articles_delete'),
    # новости
    path('news/create/', NewCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewDelete.as_view(), name='news_delete'),    
]