from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import BankAccount
from .serializers import BankAccountSerializer


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
