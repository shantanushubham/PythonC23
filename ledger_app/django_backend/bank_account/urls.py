from rest_framework.routers import SimpleRouter

from .views import BankAccountViewSet, BankTransactionViewSet

router = SimpleRouter()
router.register("bank-accounts", BankAccountViewSet, basename="bank-account")
router.register(
    "bank-transactions", BankTransactionViewSet, basename="bank-transaction"
)

urlpatterns = router.urls
