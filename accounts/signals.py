from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, MainAccountBalance, BonusAccountBalance, TotalWinnings


@receiver(post_save, sender=User)
def create_user_balances(sender, instance, created, **kwargs):
    if created:
        MainAccountBalance.objects.create(user=sender.id)
        BonusAccountBalance.objects.create(user=sender.id)


@receiver(post_save, sender=User)
def create_user_winnings(sender, instance, created, **kwargs):
    if created:
        TotalWinnings.objects.create(user=sender.id)
