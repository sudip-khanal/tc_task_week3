from django.urls import path
from apps.user import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('verify_email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('change_password/',views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:uid>/<str:token>/',views.reset_password, name='reset_password'),

]
