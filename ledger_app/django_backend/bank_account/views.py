from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import BankAccount, BankTransaction
from .serializers import BankAccountSerializer, BankTransactionSerializer


class BankAccountViewSet(viewsets.ModelViewSet):
    """
    Full CRUD on the caller's own bank accounts (a user can have many).

    GET    /api/bank-accounts/
    POST   /api/bank-accounts/
    GET    /api/bank-accounts/<id>/
    PUT    /api/bank-accounts/<id>/
    PATCH  /api/bank-accounts/<id>/
    DELETE /api/bank-accounts/<id>/

    This is financial data: everyone, staff included, only ever sees their own
    accounts through the API.
    """

    queryset = BankAccount.objects.all().order_by("id")
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BankTransactionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Bank ↔ wallet movements. Each create writes both a Transaction and a
    BankTransaction.

    POST /api/bank-transactions/
        { bank_account, direction: deposit|withdrawal, amount, remarks?, status? }
      deposit:    Transaction(sender=None, receiver=caller's wallet)
      withdrawal: Transaction(sender=caller's wallet, receiver=None)

    GET /api/bank-transactions/
    GET /api/bank-transactions/<txn_id>/
    """

    queryset = BankTransaction.objects.select_related(
        "bank_account", "transaction", "transaction__sender_wallet", "transaction__receiver_wallet"
    ).order_by("-created_at")
    serializer_class = BankTransactionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    lookup_url_kwarg = "txn_id"

    def get_queryset(self):
        return super().get_queryset().filter(bank_account__user=self.request.user)

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Bank transactions cannot be updated."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Bank transactions cannot be deleted."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
