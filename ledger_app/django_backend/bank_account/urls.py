from rest_framework.routers import SimpleRouter

from .views import BankAccountViewSet

router = SimpleRouter()
router.register("bank-accounts", BankAccountViewSet, basename="bank-account")

urlpatterns = router.urls
