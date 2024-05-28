from django.contrib import admin
from accounts.models import (
    Profile,
    MainAccountBalance,
    BonusAccountBalance,
    TotalWinnings,
)


class TotalWinningsAdmin(admin.ModelAdmin):
    list_display = ("user", "credit", "debit", "updated_at")


admin.site.register(TotalWinnings, TotalWinningsAdmin)


class MainAccountBalanceAdmin(admin.ModelAdmin):
    list_display = ("user", "credit", "debit", "updated_at")


admin.site.register(MainAccountBalance, MainAccountBalanceAdmin)


class BonusAccountBalanceAdmin(admin.ModelAdmin):
    list_display = ("user", "credit", "debit", "updated_at")


admin.site.register(BonusAccountBalance, BonusAccountBalanceAdmin)


# Register your models here.
admin.site.register(Profile)
