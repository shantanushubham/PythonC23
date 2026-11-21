from rest_framework.routers import SimpleRouter

from .views import UserViewSet

router = SimpleRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = router.urls
