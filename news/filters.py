from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from .models import Post, Category
from django.forms.widgets import DateTimeInput

# Создаем свой набор фильтров для модели Post.
class NewsFilter(FilterSet):
    
    categories = ModelChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        empty_label="Все"
    )
    
    added_after = DateTimeFilter(
        field_name='date_added',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
    
    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'title': ['icontains'],
                      
       }