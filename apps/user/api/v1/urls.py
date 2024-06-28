from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('users/reset-password/<uid>/<token>/', UserViewSet.as_view({'post': 'reset_password'}), name='user-reset-password'),

]