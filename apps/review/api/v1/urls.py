from rest_framework.routers import SimpleRouter
from apps.review.api.v1.views import ReviewViewSet
#using simple router
router = SimpleRouter()
router.register('', ReviewViewSet, basename='review')
urlpatterns = router.urls
