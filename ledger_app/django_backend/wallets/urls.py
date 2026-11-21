from rest_framework.routers import SimpleRouter

from .views import WalletViewSet

router = SimpleRouter()
router.register("wallets", WalletViewSet, basename="wallet")

urlpatterns = router.urls
