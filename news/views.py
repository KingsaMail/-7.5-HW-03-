from django.shortcuts import render

from django.views.generic import ListView, DeleteView

from .models import Post

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
    

class PostDeleteView(DeleteView):
    """Сделайте отдельную страничку для конкретной новости по адресу /news/<id новости>"""
    model = Post
    # Используем другой шаблон — new.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'
