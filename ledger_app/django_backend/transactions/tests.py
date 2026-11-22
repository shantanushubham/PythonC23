from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from wallets.models import Wallet

User = get_user_model()
PASSWORD = "Str0ng-Passw0rd!"
URL = "/api/transactions/"


class TransactionApiTests(APITestCase):
    def signup(self, email):
        r = self.client.post(
            "/api/auth/signup/",
            {"email": email, "password": PASSWORD, "confirm_password": PASSWORD},
            format="json",
        )
        return r.data["access"], User.objects.get(username=email.lower())

    def auth(self, access):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def fund(self, wallet, amount="100.00"):
        Wallet.objects.filter(pk=wallet.pk).update(balance=Decimal(amount))
        wallet.refresh_from_db()

    def setUp(self):
        self.alice_token, self.alice = self.signup("alice@example.com")
        self.bob_token, self.bob = self.signup("bob@example.com")
        self.carol_token, self.carol = self.signup("carol@example.com")
        self.fund(self.alice.wallet, "100.00")
        self.fund(self.bob.wallet, "50.00")
        self.auth(self.alice_token)

    def create(self, **overrides):
        payload = {
            "sender_wallet": self.alice.wallet.id,
            "receiver_wallet": self.bob.wallet.id,
            "amount": "25.00",
            "remarks": "lunch",
            **overrides,
        }
        return self.client.post(URL, payload, format="json")

    def test_requires_token(self):
        self.client.credentials()
        self.assertEqual(self.client.get(URL).status_code, 401)

    def test_transfer_moves_balances(self):
        r = self.create()
        self.assertEqual(r.status_code, 201)
        self.assertIsNotNone(r.data["txn_id"])
        self.assertEqual(r.data["remarks"], "lunch")
        self.alice.wallet.refresh_from_db()
        self.bob.wallet.refresh_from_db()
        self.assertEqual(self.alice.wallet.balance, Decimal("75.00"))
        self.assertEqual(self.bob.wallet.balance, Decimal("75.00"))

    def test_remarks_default_none(self):
        r = self.client.post(
            URL,
            {
                "sender_wallet": self.alice.wallet.id,
                "receiver_wallet": self.bob.wallet.id,
                "amount": "1.00",
            },
            format="json",
        )
        self.assertEqual(r.status_code, 201)
        self.assertIsNone(r.data["remarks"])

    def test_insufficient_funds(self):
        r = self.create(amount="999.00")
        self.assertEqual(r.status_code, 400)
        self.alice.wallet.refresh_from_db()
        self.assertEqual(self.alice.wallet.balance, Decimal("100.00"))

    def test_delete_not_allowed(self):
        pk = self.create().data["txn_id"]
        self.assertEqual(self.client.delete(f"{URL}{pk}/").status_code, 405)

    def test_list_shows_sent_and_received(self):
        self.create()
        self.auth(self.bob_token)
        self.create(
            sender_wallet=self.bob.wallet.id,
            receiver_wallet=self.alice.wallet.id,
            amount="5.00",
        )
        self.assertEqual(self.client.get(URL).data["count"], 2)

        self.auth(self.carol_token)
        self.assertEqual(self.client.get(URL).data["count"], 0)

    def test_cannot_touch_unrelated_transaction(self):
        pk = self.create().data["txn_id"]
        self.auth(self.carol_token)
        self.assertEqual(self.client.get(f"{URL}{pk}/").status_code, 404)
