from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from .models import Post


class PostFilter(FilterSet):
    date = DateFilter(
        field_name='time_in', widget=DateInput(attrs={'type': 'date'}), label='Поиск по дате', lookup_expr='date__gte'
    )


    class Meta:
        model = Post
        fields = {
            # поиск по названию
            'article': ['icontains'],
            'name_author': ['icontains'],
            #'text': ['incontains'],
        }