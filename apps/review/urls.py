from django.urls import path
from apps.review import views

urlpatterns = [
    path('create_review/', views.create_review, name='create-review'),

]