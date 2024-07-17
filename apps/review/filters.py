import django_filters
from django.contrib.auth.models import User

from .models import Review
from apps.book.models import Book


class ReviewFilter(django_filters.FilterSet):
    book = django_filters.ModelChoiceFilter(queryset=Book.objects.all())
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    review_text = django_filters.CharFilter(field_name='review_text',lookup_expr='iexact')
    class Meta:
        model = Review
        fields = ['book', 'user', 'review_text']
