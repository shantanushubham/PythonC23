from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Transaction
from .serializers import TransactionListSerializer, TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    Wallet-to-wallet transfers involving the caller's wallet.

    GET    /api/transactions/
    POST   /api/transactions/
    GET    /api/transactions/<txn_id>/
    PUT/PATCH /api/transactions/<txn_id>/
    DELETE /api/transactions/<txn_id>/  (pending only → cancelled)
    """

    queryset = None
    permission_classes = [IsAuthenticated]
    lookup_field = "txn_id"

    def get_serializer_class(self):
        if self.action == "list":
            return TransactionListSerializer
        return TransactionSerializer

    def get_queryset(self):

        # user = the logged in user
        # Transaction.objects.filter(where user = sender or receiver)
        # Q aka Query Expression
        # | is OR
        # Transaction.objects.filter(Q(sender_wallet__user=user) | Q(receiver_wallet__user=user))

        # SELECT * FROM (
        #     SELECT * FROM transactions
        #     LEFT JOIN wallets
        #     ON transactions.sender_wallet_id = wallets.id OR transactions.receiver_wallet_id = wallets.id
        # ) WHERE user_id = user.id

        user = self.request.user
        return (
            Transaction.objects.select_related("sender_wallet", "receiver_wallet")
            # filter transactions where the caller is the sender or receiver
            .filter(Q(sender_wallet__user=user) | Q(receiver_wallet__user=user))
        )

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Ashish - 5,000
# Raj - 10,000
# Shantanu - 1,000

# X1: Ashish -> Shantanu : 2000 (T=1) M1
# X2: Raj -> Shantanu : 1000 (T=1) M2

# S1: Deduction from Sender's wallet -- X1, X2
# S2: Addition to Receiver's wallet -- X1 (S=3k), X2 (S=2k)
# S3: Create a transaction record -- X1, X2

# function update_wallet_balance(sender_id, receiver_id, amount):
#     CRTITICAL SECTION - the peice of code which can cause race condition 
#   LOCK { START
#     S1: read the balance of sender and receiver
#     S2: update the balance of sender and receiver
#     S3: write the balance of sender and receiver to the database
#   } END

# ____________________________________________________________
# T=0     # T=1
# A=5k    # A=3k
# S=1k    # S=2k
# R=10k   # R=9k

# This problem can be fixed by 2 methods:
# 1. Use Locks in the program by using Multi-threading
# 2. Use Locks in the database by using Database Locking
