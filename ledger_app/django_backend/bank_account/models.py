from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class BankAccount(models.Model):
    """A bank account owned by a user. A user can have many."""

    class AccountType(models.TextChoices):
        SAVINGS = "savings", "Savings"
        CURRENT = "current", "Current"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bank_accounts",
    )
    account_holder_name = models.CharField(max_length=150)
    bank_name = models.CharField(max_length=150)
    account_number = models.CharField(
        max_length=18,
        validators=[
            RegexValidator(r"^\d{9,18}$", "Account number must be 9 to 18 digits.")
        ],
    )
    ifsc_code = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                r"^[A-Z]{4}0[A-Z0-9]{6}$", "Enter a valid 11-character IFSC code."
            )
        ],
    )
    account_type = models.CharField(
        max_length=10, choices=AccountType.choices, default=AccountType.SAVINGS
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bank_accounts"
        ordering = ["id"]
        constraints = [
            # The same account can't be linked twice by the same user.
            models.UniqueConstraint(
                fields=["user", "ifsc_code", "account_number"],
                name="unique_bank_account_per_user",
            ),
        ]

    def save(self, *args, **kwargs):
        self.ifsc_code = self.ifsc_code.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bank_name} ****{self.account_number[-4:]}"
