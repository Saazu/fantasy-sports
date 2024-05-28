from rest_framework import serializers
from .models import MainAccountBalance, BonusAccountBalance, Profile, TotalWinnings
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.exceptions import ValidationError


class TotalWinningsSerializer(serializers.ModelSerializer):
    wallet_details = serializers.SerializerMethodField(read_only=True)
    source_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TotalWinnings
        fields = (
            "latest",
            "user",
            "debit",
            "credit",
            "source",
            "wallet_credited",
            "wallet_details",
            "source_details",
        )
        read_only_fields = ("latest",)
        extra_kwargs = {
            "source": {"write_only": True},
            "wallet_credited": {"write_only": True},
        }

    def get_wallet_details(self, obj):
        return obj.wallet_credited

    def get_source_details(self, obj):
        return obj.source

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        debit = attrs.get("debit")
        credit = attrs.get("credit")
        wallet_credited = attrs.get("wallet_credited")
        source = attrs.get("source")
        if debit != 0 and credit != 0:
            raise ValidationError("Cannot credit and debit in the same transaction")
        if source == "paid_game" and wallet_credited != "main_account_balance":
            raise ValidationError("Winnings for paid games must go to main wallet")
        elif source != "paid_game" and wallet_credited != "bonus_account_balance":
            raise ValidationError("Winnings for free games must go to bonus wallet")

        return validated_data


class AccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainAccountBalance
        fields = ("credit", "debit", "balance", "user")


class BonusBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusAccountBalance
        fields = ("credit", "debit", "balance", "user")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "date_joined")


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    user = UserSerializer(read_only=True)
    main_balance = serializers.SerializerMethodField()
    bonus_balance = serializers.SerializerMethodField()
    total_winnings = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "user",
            "username",
            "name",
            "email",
            "password",
            "main_phone_number",
            "momo_phone_number",
            "total_winnings",
            "main_balance",
            "bonus_balance",
        )

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        new_user = User.objects.create(
            username=username, email=email, password=password
        )
        with transaction.atomic():
            TotalWinnings.objects.create(user=new_user)
            MainAccountBalance.objects.create(user=new_user)
            BonusAccountBalance.objects.create(user=new_user)
            return Profile.objects.create(user=new_user, **validated_data)

    def get_main_balance(self, obj):
        latest_main_balance = MainAccountBalance.objects.filter(user=obj.user).latest(
            "updated_at"
        )
        serializer = AccountBalanceSerializer(instance=latest_main_balance, many=False)
        return serializer.data.get("balance")

    def get_bonus_balance(self, obj):
        latest_bonus_balance = BonusAccountBalance.objects.filter(user=obj.user).latest(
            "updated_at"
        )
        serializer = BonusBalanceSerializer(instance=latest_bonus_balance, many=False)
        return serializer.data.get("balance")

    def get_total_winnings(self, obj):
        latest_total_winnings = TotalWinnings.objects.filter(user=obj.user).latest(
            "updated_at"
        )
        serializer = TotalWinningsSerializer(instance=latest_total_winnings, many=False)
        return serializer.data.get("latest")
