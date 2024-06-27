from apps.review.api.v1.views import ReviewViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', ReviewViewSet, basename='review')
urlpatterns = router.urls
