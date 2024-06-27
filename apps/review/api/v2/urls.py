from django.urls import path
from apps.review.api.v2 import views

review_list = views.ReviewViewSet.as_view({
    'get': 'list'
})
review_detail =views.ReviewViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('reviews/', review_list, name='review_list'),
    path('review_detail/<int:pk>/', review_detail, name='review_detail'),
]

