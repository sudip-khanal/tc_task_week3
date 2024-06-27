# example of model mixins
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin,ListModelMixin,
                                   RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin)
from rest_framework.permissions import IsAuthenticated
from apps.book.models import Book
from apps.book.serializers import BookSerializer


class Create_or_ListViewSet(CreateModelMixin,ListModelMixin,GenericAPIView):
    queryset=Book.objects.filter(is_active=True)
    serializer_class=BookSerializer
    permission_classes=[IsAuthenticated]

    def get(self,request,*args, **kwargs):
        return self.list(request,*args, **kwargs)
    
    def post(self,request,*args, **kwargs):
        return self.create(request,*args, **kwargs)
    
class Retrive_Update_Delete_ViewSet(RetrieveModelMixin,UpdateModelMixin,
                                    DestroyModelMixin,GenericAPIView):
    queryset=Book.objects.filter(is_active=True)
    serializer_class=BookSerializer
    permission_classes=[IsAuthenticated]


    def get(self,request,*args, **kwargs):
        return self.retrieve(request,*args, **kwargs)
    
    def put(self,request,*args, **kwargs):
        return self.update(request,*args, **kwargs)
    
    def delete(self,request,*args, **kwargs):
        return self.destroy(request,*args, **kwargs)
   
    