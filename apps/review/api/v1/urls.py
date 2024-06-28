from rest_framework.routers import SimpleRouter
from apps.review.api.v1.views import ReviewViewSet

router = SimpleRouter()
router.register('', ReviewViewSet, basename='review')
urlpatterns = router.urls
