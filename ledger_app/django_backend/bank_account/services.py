from decimal import Decimal

from django.db import transaction as db_transaction
from rest_framework.exceptions import ValidationError

from transactions.models import Transaction
from wallets.models import Wallet

from .models import BankTransaction


@db_transaction.atomic
def create_bank_transaction(
    *,
    user,
    bank_account,
    amount: Decimal,
    direction: str,
    remarks=None,
    status=BankTransaction.Status.COMPLETED,
):
    """
    Create both a Transaction and a BankTransaction.

    deposit:    sender=None, receiver=user.wallet  (credit wallet)
    withdrawal: sender=user.wallet, receiver=None  (debit wallet)
    """
    if bank_account.user_id != user.id:
        raise ValidationError(
            {"bank_account": "You can only use your own bank account."}
        )
    if amount <= 0:
        raise ValidationError({"amount": "Amount must be greater than zero."})
    if direction not in BankTransaction.Direction.values:
        raise ValidationError({"direction": "Must be deposit or withdrawal."})
    if status not in (
        BankTransaction.Status.PENDING,
        BankTransaction.Status.COMPLETED,
    ):
        raise ValidationError(
            {"status": "New bank transactions must be pending or completed."}
        )

    wallet = Wallet.objects.select_for_update().get(pk=user.wallet.pk)

    if direction == BankTransaction.Direction.DEPOSIT:
        if status == BankTransaction.Status.COMPLETED:
            wallet.balance += amount
            wallet.save(update_fields=["balance", "updated_at"])
        txn = Transaction.objects.create(
            sender_wallet=None,
            receiver_wallet=wallet,
            amount=amount,
            remarks=remarks,
        )
    else:
        if status == BankTransaction.Status.COMPLETED:
            if wallet.balance < amount:
                raise ValidationError(
                    {"amount": "Insufficient balance in the wallet."}
                )
            wallet.balance -= amount
            wallet.save(update_fields=["balance", "updated_at"])
        txn = Transaction.objects.create(
            sender_wallet=wallet,
            receiver_wallet=None,
            amount=amount,
            remarks=remarks,
        )

    return BankTransaction.objects.create(
        transaction=txn,
        bank_account=bank_account,
        direction=direction,
        status=status,
    )
