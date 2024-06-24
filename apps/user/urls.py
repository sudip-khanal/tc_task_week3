from django.urls import path
from apps.user import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('verify-email/<uidb64>/<token>/',views.verify_email, name='verify-email'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('change-password/',views.change_password, name='change-password'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/<str:uidb64>/<str:token>/',views.reset_password, name='reset-password'),

]
