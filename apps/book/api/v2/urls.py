from django.urls import path
from apps.book.api.v2 import views
# class based views url patterns
urlpatterns=[
    path('',views.Create_or_ListViewSet.as_view()),
    path('<int:pk>/',views.Retrive_Update_Delete_ViewSet.as_view()),

]