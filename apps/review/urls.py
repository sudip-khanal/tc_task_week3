# from django.urls import path
# from apps.review import views

# urlpatterns = [
#     path('create_review/', views.create_review, name='create-review'),

# ]

from apps.review.views import ReviewViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', ReviewViewSet, basename='review')
urlpatterns = router.urls
