from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book-list'),
    path('create_book/', views.book_create, name='create_book'),
    path('book/<int:pk>/', views.book_detail, name='book-detail'),
    path('update_book/<int:pk>/', views.book_update, name='update_book'),
    path('delete_book/<int:pk>/', views.book_soft_delete, name='delete_book'),
    ##favorite books
    path('favourite-book/', views.favourite_book, name='favourite-book'),
    path('create-favourite/', views.create_favourite, name='create-favourite'),
    #path('delete-favourite/<int:pk>/',views.favorite_delete, name='favorite-delete'),

]
