from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from rest_framework.test import APITestCase

from .models import Wallet

User = get_user_model()
PASSWORD = "Str0ng-Passw0rd!"


class WalletTests(APITestCase):
    def signup(self, email="test@example.com"):
        return self.client.post(
            "/api/auth/signup/",
            {"email": email, "password": PASSWORD, "confirm_password": PASSWORD},
            format="json",
        )

    def auth(self, access):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_wallet_created_on_signup(self):
        self.assertEqual(self.signup().status_code, 201)
        user = User.objects.get()
        self.assertEqual(Wallet.objects.filter(user=user).count(), 1)
        self.assertEqual(user.wallet.balance, 0)

    def test_wallet_created_for_any_user_creation_path(self):
        u = User.objects.create_user(username="a@example.com", password=PASSWORD)
        s = User.objects.create_superuser(username="b@example.com", password=PASSWORD)
        self.assertTrue(Wallet.objects.filter(user=u).exists())
        self.assertTrue(Wallet.objects.filter(user=s).exists())

    def test_saving_existing_user_does_not_create_second_wallet(self):
        u = User.objects.create_user(username="a@example.com", password=PASSWORD)
        u.first_name = "x"
        u.save()
        self.assertEqual(Wallet.objects.filter(user=u).count(), 1)

    def test_one_wallet_per_user_enforced_by_db(self):
        u = User.objects.create_user(username="a@example.com", password=PASSWORD)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Wallet.objects.create(user=u)

    def test_negative_balance_rejected_by_db(self):
        u = User.objects.create_user(username="a@example.com", password=PASSWORD)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Wallet.objects.filter(user=u).update(balance=-1)

    def test_wallet_api_requires_token(self):
        self.assertEqual(self.client.get("/api/wallets/").status_code, 401)

    def test_me_and_scoping(self):
        self.signup("other@example.com")
        self.auth(self.signup().data["access"])
        r = self.client.get("/api/wallets/me/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["email"], "test@example.com")
        self.assertEqual(str(r.data["balance"]), "0.00")
        self.assertEqual(self.client.get("/api/wallets/").data["count"], 1)
        other = Wallet.objects.get(user__username="other@example.com")
        self.assertEqual(self.client.get(f"/api/wallets/{other.pk}/").status_code, 404)

    def test_wallet_is_read_only_via_api(self):
        self.auth(self.signup().data["access"])
        w = Wallet.objects.get()
        self.assertEqual(self.client.post("/api/wallets/", {}).status_code, 405)
        self.assertEqual(
            self.client.patch(f"/api/wallets/{w.pk}/", {"balance": "999"}).status_code, 405
        )
        self.assertEqual(self.client.delete(f"/api/wallets/{w.pk}/").status_code, 405)
