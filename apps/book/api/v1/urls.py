from rest_framework.routers import DefaultRouter
from apps.book.api.v1.views import BookViewSet
# Default router 
router = DefaultRouter()
router.register('', BookViewSet, basename='book')
urlpatterns = router.urls
