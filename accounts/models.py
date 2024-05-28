from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Core(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccountBalance(Core):
    credit = models.IntegerField(default=0)
    debit = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TotalWinnings(Core):

    PAID_GAME = "paid_game"
    FREE_GAME = "free_game"
    PROMO = "promo"
    SOURCE_CHOICES = {
        PAID_GAME: "Paid Game",
        FREE_GAME: "Free Game",
        PROMO: "Promo",
    }

    MAIN_ACCOUNT = "main_account_balance"
    BONUS_ACCOUNT = "bonus_account_balance"
    WALLET_CHOICES = {
        MAIN_ACCOUNT: "Main Account",
        BONUS_ACCOUNT: "Bonus Account",
    }

    latest = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    debit = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    source = models.CharField(max_length=254, choices=SOURCE_CHOICES.items())
    wallet_credited = models.CharField(max_length=254, choices=WALLET_CHOICES.items())

    class Meta:
        verbose_name_plural = "Total Winnings"


class MainAccountBalance(AccountBalance):
    pass


class BonusAccountBalance(AccountBalance):
    pass


class Profile(Core):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    main_phone_number = models.CharField(max_length=20)
    momo_phone_number = models.CharField(max_length=20)
