from django.urls import path
from apps.review import views

urlpatterns = [
    path('create_review/', views.create_review, name='create-review'),
    path('list_review/',views.list_review,name='list_review'),

]

