from apps.review.api.views import ReviewViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', ReviewViewSet, basename='review')
urlpatterns = router.urls
