from rest_framework.test import APITestCase

from .models import BankAccount

PASSWORD = "Str0ng-Passw0rd!"
BANK_ACCOUNT_URL = "/api/bank-accounts/"

PAYLOAD = {
    "account_holder_name": "Test User",
    "bank_name": "HDFC Bank",
    "account_number": "123456789012",
    "ifsc_code": "hdfc0001234",
    "account_type": "savings",
}


class BankAccountApiTests(APITestCase):
    def signup(self, email):
        r = self.client.post(
            "/api/auth/signup/",
            {"email": email, "password": PASSWORD, "confirm_password": PASSWORD},
            format="json",
        )
        return r.data["access"]

    def auth(self, access):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def setUp(self):
        self.alice = self.signup("alice@example.com")
        self.bob = self.signup("bob@example.com")
        self.auth(self.alice)

    def create(self, **overrides):
        return self.client.post(BANK_ACCOUNT_URL, {**PAYLOAD, **overrides}, format="json")

    def test_requires_token(self):
        self.client.credentials()
        self.assertEqual(self.client.get(BANK_ACCOUNT_URL).status_code, 401)
        self.assertEqual(self.client.post(BANK_ACCOUNT_URL, PAYLOAD, format="json").status_code, 401)

    def test_create_uses_request_user_and_normalizes_ifsc(self):
        r = self.create()
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["ifsc_code"], "HDFC0001234")
        acct = BankAccount.objects.get()
        self.assertEqual(acct.user.username, "alice@example.com")

    def test_owner_cannot_be_spoofed(self):
        r = self.create(user=999)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(BankAccount.objects.get().user.username, "alice@example.com")

    def test_user_can_have_multiple_accounts(self):
        self.assertEqual(self.create().status_code, 201)
        self.assertEqual(self.create(account_number="999999999999").status_code, 201)
        self.assertEqual(self.client.get(BANK_ACCOUNT_URL).data["count"], 2)

    def test_same_account_twice_rejected(self):
        self.create()
        self.assertEqual(self.create(ifsc_code="HDFC0001234").status_code, 400)

    def test_two_users_may_link_the_same_account(self):
        self.create()
        self.auth(self.bob)
        self.assertEqual(self.create().status_code, 201)

    def test_validation(self):
        self.assertEqual(self.create(account_number="12ab").status_code, 400)
        self.assertEqual(self.create(ifsc_code="BAD").status_code, 400)
        self.assertEqual(self.create(account_type="crypto").status_code, 400)

    def test_retrieve_update_delete(self):
        pk = self.create().data["id"]
        self.assertEqual(self.client.get(f"{BANK_ACCOUNT_URL}{pk}/").status_code, 200)

        r = self.client.patch(f"{BANK_ACCOUNT_URL}{pk}/", {"bank_name": "ICICI"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["bank_name"], "ICICI")

        r = self.client.put(
            f"{BANK_ACCOUNT_URL}{pk}/", {**PAYLOAD, "bank_name": "SBI"}, format="json"
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(BankAccount.objects.get().bank_name, "SBI")

        self.assertEqual(self.client.delete(f"{BANK_ACCOUNT_URL}{pk}/").status_code, 204)
        self.assertFalse(BankAccount.objects.exists())

    def test_cannot_touch_other_users_accounts(self):
        pk = self.create().data["id"]
        self.auth(self.bob)
        self.assertEqual(self.client.get(BANK_ACCOUNT_URL).data["count"], 0)
        self.assertEqual(self.client.get(f"{BANK_ACCOUNT_URL}{pk}/").status_code, 404)
        self.assertEqual(
            self.client.patch(f"{BANK_ACCOUNT_URL}{pk}/", {"bank_name": "X"}, format="json").status_code,
            404,
        )
        self.assertEqual(self.client.delete(f"{BANK_ACCOUNT_URL}{pk}/").status_code, 404)
        self.assertTrue(BankAccount.objects.filter(pk=pk).exists())
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from transactions.models import Transaction
from wallets.models import Wallet

from .models import BankAccount, BankTransaction

User = get_user_model()
PASSWORD = "Str0ng-Passw0rd!"
BANK_TXN_URL = "/api/bank-transactions/"


class BankTransactionApiTests(APITestCase):
    def signup(self, email):
        r = self.client.post(
            "/api/auth/signup/",
            {"email": email, "password": PASSWORD, "confirm_password": PASSWORD},
            format="json",
        )
        return r.data["access"], User.objects.get(username=email.lower())

    def auth(self, access):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def add_bank_account(self, user, number="123456789012"):
        return BankAccount.objects.create(
            user=user,
            account_holder_name="Test",
            bank_name="HDFC Bank",
            account_number=number,
            ifsc_code="HDFC0001234",
        )

    def setUp(self):
        self.alice_token, self.alice = self.signup("alice@example.com")
        self.bob_token, self.bob = self.signup("bob@example.com")
        self.alice_bank = self.add_bank_account(self.alice)
        self.bob_bank = self.add_bank_account(self.bob, number="999999999999")
        self.auth(self.alice_token)

    def create(self, **overrides):
        payload = {
            "bank_account": self.alice_bank.id,
            "direction": "deposit",
            "amount": "50.00",
            **overrides,
        }
        return self.client.post(BANK_TXN_URL, payload, format="json")

    def test_requires_token(self):
        self.client.credentials()
        self.assertEqual(self.client.get(BANK_TXN_URL).status_code, 401)

    def test_deposit_creates_transaction_and_bank_transaction(self):
        r = self.create(direction="deposit", amount="50.00")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["direction"], "deposit")
        self.assertEqual(r.data["status"], "completed")
        self.assertIsNone(r.data["sender_wallet"])
        self.assertEqual(r.data["receiver_wallet"], self.alice.wallet.id)
        self.assertEqual(r.data["amount"], "50.00")

        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(BankTransaction.objects.count(), 1)
        txn = Transaction.objects.get()
        bank_txn = BankTransaction.objects.get()
        self.assertEqual(bank_txn.pk, txn.txn_id)
        self.assertIsNone(txn.sender_wallet_id)
        self.assertEqual(txn.receiver_wallet_id, self.alice.wallet.id)

        self.alice.wallet.refresh_from_db()
        self.assertEqual(self.alice.wallet.balance, Decimal("50.00"))

    def test_withdrawal_creates_transaction_with_receiver_none(self):
        Wallet.objects.filter(pk=self.alice.wallet.id).update(balance=Decimal("100.00"))
        r = self.create(direction="withdrawal", amount="40.00", remarks="atm")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["sender_wallet"], self.alice.wallet.id)
        self.assertIsNone(r.data["receiver_wallet"])
        self.assertEqual(r.data["remarks"], "atm")

        self.alice.wallet.refresh_from_db()
        self.assertEqual(self.alice.wallet.balance, Decimal("60.00"))

    def test_withdrawal_insufficient_funds(self):
        r = self.create(direction="withdrawal", amount="10.00")
        self.assertEqual(r.status_code, 400)
        self.assertFalse(Transaction.objects.exists())
        self.assertFalse(BankTransaction.objects.exists())

    def test_cannot_use_someone_elses_bank_account(self):
        r = self.create(bank_account=self.bob_bank.id)
        self.assertEqual(r.status_code, 400)

    def test_pending_deposit_does_not_move_balance(self):
        r = self.create(status="pending", amount="25.00")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["status"], "pending")
        self.alice.wallet.refresh_from_db()
        self.assertEqual(self.alice.wallet.balance, Decimal("0.00"))
        self.assertTrue(Transaction.objects.exists())
        self.assertTrue(BankTransaction.objects.exists())

    def test_list_scoped_to_caller(self):
        self.create()
        self.auth(self.bob_token)
        self.create(bank_account=self.bob_bank.id)
        self.assertEqual(self.client.get(BANK_TXN_URL).data["count"], 1)

    def test_update_and_delete_not_allowed(self):
        pk = self.create().data["txn_id"]
        self.assertEqual(
            self.client.patch(f"{BANK_TXN_URL}{pk}/", {"status": "failed"}, format="json").status_code,
            405,
        )
        self.assertEqual(self.client.delete(f"{BANK_TXN_URL}{pk}/").status_code, 405)
