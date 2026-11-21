from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()

PASSWORD = "Str0ng-Passw0rd!"


class UserApiTests(APITestCase):
    def signup(self, email="Test@Example.com"):
        return self.client.post(
            "/api/auth/signup/",
            {"email": email, "password": PASSWORD, "confirm_password": PASSWORD},
            format="json",
        )

    def auth(self, access):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_protected_endpoints_need_token(self):
        self.assertEqual(self.client.get("/api/users/me/").status_code, 401)
        self.assertEqual(self.client.get("/api/users/").status_code, 401)

    def test_me_update_syncs_email_and_username(self):
        self.auth(self.signup().data["access"])
        r = self.client.patch(
            "/api/users/me/", {"email": "New@Example.com"}, format="json"
        )
        self.assertEqual(r.status_code, 200)
        user = User.objects.get()
        self.assertEqual(user.username, "new@example.com")
        self.assertEqual(user.email, "new@example.com")

    def test_user_only_sees_self(self):
        self.signup("other@example.com")
        self.auth(self.signup().data["access"])
        r = self.client.get("/api/users/")
        self.assertEqual(r.data["count"], 1)
        other = User.objects.get(username="other@example.com")
        self.assertEqual(self.client.get(f"/api/users/{other.pk}/").status_code, 404)

    def test_create_via_viewset_disabled(self):
        self.auth(self.signup().data["access"])
        self.assertEqual(self.client.post("/api/users/", {}).status_code, 405)

    def test_delete_is_soft(self):
        self.auth(self.signup().data["access"])
        user = User.objects.get()
        self.assertEqual(self.client.delete(f"/api/users/{user.pk}/").status_code, 204)
        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def test_createsuperuser_with_default_manager(self):
        admin = User.objects.create_superuser(
            username="Admin@Example.com", password=PASSWORD
        )
        self.assertEqual(admin.username, "admin@example.com")
        self.assertEqual(admin.email, "admin@example.com")
        self.assertTrue(admin.is_staff and admin.is_superuser)
