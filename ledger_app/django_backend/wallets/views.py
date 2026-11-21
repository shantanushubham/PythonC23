from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Wallet
from .serializers import WalletSerializer


class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only: wallets are created automatically with the user, and balances
    change only through ledger transactions.

    GET /api/wallets/      - the caller's wallet (staff: all wallets)
    GET /api/wallets/<id>/ - a single wallet
    GET /api/wallets/me/   - the caller's wallet
    """

    queryset = Wallet.objects.select_related("user").order_by("id")
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs if user.is_staff else qs.filter(user=user)

    @action(detail=False, methods=["get"])
    def me(self, request):
        return Response(self.get_serializer(request.user.wallet).data)
