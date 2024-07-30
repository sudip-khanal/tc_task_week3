import django_filters
from apps.book.models import Book


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author', lookup_expr='iexact')
    created_at_gt = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gt')
    created_at_lt = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lt')
    user = django_filters.CharFilter(method='filter_by_user')

    class Meta:
        model = Book
        fields = ['title', 'author', 'created_at', 'created_at_lt', 'user']

    def filter_by_user(self, queryset,name,value):
        return queryset.filter(created_by__username=value)
