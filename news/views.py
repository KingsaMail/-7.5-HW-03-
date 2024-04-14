import datetime
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from requests import request

from .models import Author, Post
from .filters import NewsFilter
from .forms import PostArticleCreate
from pprint import pprint 

class PostListView(ListView):
    """Сделайте новую страничку с адресом /news/, на которой должен выводиться список всех новостей."""
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_added'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10 # количество записей на странице
    
    
class PostListFilter(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_added'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_filter.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10 # количество записей на странице
    
    # Переопределяем функцию получения списка статей(новостей)
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список статей(новостей)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       #context['time_now'] = datetime.utcnow()
       return context
    

class PostDetailView(DetailView):
    """Сделайте отдельную страничку для конкретной новости по адресу /news/<id новости>"""
    model = Post
    # Используем другой шаблон — new.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем пост.статья
    context_object_name = 'new'    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Post.objects.get(pk=self.kwargs['pk']).categories.values_list('category', flat=True)
        return context
    

class ArtCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('news.add_post',)
    # Указываем нашу разработанную форму
    form_class = PostArticleCreate
    # модель статьи
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'postartcreate.html'
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = Author.objects.get(user=self.request.user)
        instance.save()
        
        return super().form_valid(form)
    
    
# Добавляем представление для изменения статьи.
class ArtEdit(PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('news.change_post',)    
    form_class = PostArticleCreate
    model = Post
    template_name = 'postartcreate.html'
    
    
class ArtDelete(PermissionRequiredMixin, DeleteView):    
    raise_exception = True
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news:news')
    
    
class NewCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('news.add_post',)
    # Указываем нашу разработанную форму
    form_class = PostArticleCreate
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'postartcreate.html'
    
    # def form_valid(self, form):
    #     news = form.save(commit=False)
    #     news.post = 'news'
    #     return super().form_valid(form)
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        # print(self.request.user)
        instance.user = Author.objects.get(user=self.request.user)
        instance.post = 'news'
        instance.save()
        
        return super().form_valid(form)
    
    
    
class NewEdit(PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('news.change_post',)
    form_class = PostArticleCreate
    model = Post
    template_name = 'postartcreate.html'
    
    
class NewDelete(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news:news')
