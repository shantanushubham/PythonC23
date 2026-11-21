from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction


class User(AbstractUser):
    """
    AbstractUser where username *is* the email.

    The default Django manager is used (no custom manager). `username` is
    redefined as a unique EmailField and `email` is kept in sync with it.
    Every new user also gets exactly one wallet (see save()).
    """

    username = models.EmailField("email address", unique=True)

    class Meta:
        db_table = "users"

    def save(self, *args, **kwargs):
        self.username = self.username.strip().lower()
        self.email = self.username
        update_fields = kwargs.get("update_fields")
        if update_fields is not None and "username" in update_fields:
            kwargs["update_fields"] = {*update_fields, "email"}

        is_new = self._state.adding
        # Atomic: the user and its wallet are committed together or not at all.
        with transaction.atomic():
            super().save(*args, **kwargs)
            if is_new:
                # Looked up lazily to avoid a circular import with wallets.
                Wallet = apps.get_model("wallets", "Wallet") ## Equivalent to from wallets.models import Wallet
                Wallet.objects.create(user=self)

    def __str__(self):
        return self.username
