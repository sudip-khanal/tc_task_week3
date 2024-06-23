from django.urls import path
from apps.user import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('verify-email/<uidb64>/<token>/',views.verify_email, name='verify-email'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('change-password/',views.change_password, name='change-password'),

]
