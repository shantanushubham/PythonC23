from rest_framework.test import APITestCase

from .models import BankAccount

PASSWORD = "Str0ng-Passw0rd!"
URL = "/api/bank-accounts/"

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
        return self.client.post(URL, {**PAYLOAD, **overrides}, format="json")

    def test_requires_token(self):
        self.client.credentials()
        self.assertEqual(self.client.get(URL).status_code, 401)
        self.assertEqual(self.client.post(URL, PAYLOAD, format="json").status_code, 401)

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
        self.assertEqual(self.client.get(URL).data["count"], 2)

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
        self.assertEqual(self.client.get(f"{URL}{pk}/").status_code, 200)

        r = self.client.patch(f"{URL}{pk}/", {"bank_name": "ICICI"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["bank_name"], "ICICI")

        r = self.client.put(
            f"{URL}{pk}/", {**PAYLOAD, "bank_name": "SBI"}, format="json"
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(BankAccount.objects.get().bank_name, "SBI")

        self.assertEqual(self.client.delete(f"{URL}{pk}/").status_code, 204)
        self.assertFalse(BankAccount.objects.exists())

    def test_cannot_touch_other_users_accounts(self):
        pk = self.create().data["id"]
        self.auth(self.bob)
        self.assertEqual(self.client.get(URL).data["count"], 0)
        self.assertEqual(self.client.get(f"{URL}{pk}/").status_code, 404)
        self.assertEqual(
            self.client.patch(f"{URL}{pk}/", {"bank_name": "X"}, format="json").status_code,
            404,
        )
        self.assertEqual(self.client.delete(f"{URL}{pk}/").status_code, 404)
        self.assertTrue(BankAccount.objects.filter(pk=pk).exists())
