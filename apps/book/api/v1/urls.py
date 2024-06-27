
from apps.book.api.v1.views import BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', BookViewSet, basename='book')
urlpatterns = router.urls
