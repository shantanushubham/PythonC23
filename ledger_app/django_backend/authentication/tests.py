from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()

PASSWORD = "Str0ng-Passw0rd!"


class AuthApiTests(APITestCase):
    def signup(self, email="Test@Example.com"):
        return self.client.post(
            "/api/auth/signup/",
            {
                "email": email,
                "password": PASSWORD,
                "confirm_password": PASSWORD,
                "first_name": "Test",
            },
            format="json",
        )

    def login(self, email="test@example.com", password=PASSWORD):
        return self.client.post(
            "/api/auth/login/", {"email": email, "password": password}, format="json"
        )

    def auth(self, access):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_signup_returns_tokens_and_uses_email_as_username(self):
        r = self.signup()
        self.assertEqual(r.status_code, 201)
        self.assertIn("access", r.data)
        self.assertIn("refresh", r.data)
        self.assertNotIn("password", r.data["user"])
        user = User.objects.get(username="test@example.com")
        self.assertEqual(user.email, "test@example.com")

    def test_password_is_bcrypt_hashed(self):
        self.signup()
        user = User.objects.get(username="test@example.com")
        self.assertTrue(user.password.startswith("bcrypt_sha256$"))

    def test_duplicate_email_rejected_case_insensitive(self):
        self.signup()
        self.assertEqual(self.signup("TEST@example.com").status_code, 400)

    def test_password_mismatch_rejected(self):
        r = self.client.post(
            "/api/auth/signup/",
            {"email": "a@b.com", "password": PASSWORD, "confirm_password": "x"},
            format="json",
        )
        self.assertEqual(r.status_code, 400)

    def test_login(self):
        self.signup()
        self.assertEqual(self.login(password="wrong").status_code, 400)
        r = self.login(email="TEST@example.com")
        self.assertEqual(r.status_code, 200)
        self.assertIn("access", r.data)
        self.assertIn("refresh", r.data)

    def test_change_password(self):
        self.auth(self.signup().data["access"])
        new = "An0ther-Str0ng-Pw!"
        r = self.client.post(
            "/api/auth/change-password/",
            {"old_password": PASSWORD, "new_password": new},
            format="json",
        )
        self.assertEqual(r.status_code, 200)
        self.client.credentials()
        self.assertEqual(self.login(password=PASSWORD).status_code, 400)
        self.assertEqual(self.login(password=new).status_code, 200)

    def test_change_password_requires_token(self):
        r = self.client.post("/api/auth/change-password/", {}, format="json")
        self.assertEqual(r.status_code, 401)

    def test_refresh_and_logout_blacklists_token(self):
        data = self.signup().data
        r = self.client.post(
            "/api/auth/refresh/", {"refresh": data["refresh"]}, format="json"
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn("access", r.data)
        new_refresh = r.data["refresh"]  # ROTATE_REFRESH_TOKENS is on

        self.auth(data["access"])
        r = self.client.post(
            "/api/auth/logout/", {"refresh": new_refresh}, format="json"
        )
        self.assertEqual(r.status_code, 205)
        self.client.credentials()
        r = self.client.post(
            "/api/auth/refresh/", {"refresh": new_refresh}, format="json"
        )
        self.assertEqual(r.status_code, 401)

    def test_deleted_user_cannot_login(self):
        self.auth(self.signup().data["access"])
        user = User.objects.get()
        self.client.delete(f"/api/users/{user.pk}/")
        self.client.credentials()
        self.assertEqual(self.login().status_code, 400)
