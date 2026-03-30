from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Типи акаунтів
    BASIC = 'basic'
    PREMIUM = 'premium'
    ACCOUNT_TYPE_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
    ]

    # Ролі користувачів
    BUYER = 'buyer'
    SELLER = 'seller'
    MANAGER = 'manager'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
        (MANAGER, 'Manager'),
        (ADMIN, 'Admin'),
    ]

    # Додаткові поля понад стандартний User
    # blank=False означає що поле обов'язкове
    phone = models.CharField(max_length=20, blank=True)

    # Роль користувача — за замовчуванням buyer
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=BUYER,
    )

    # Тип акаунту — за замовчуванням basic
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default=BASIC,
    )

    # Чи верифікований акаунт менеджером
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} ({self.role} / {self.account_type})'

    # Зручні властивості для перевірки ролі в коді
    @property
    def is_seller(self):
        return self.role == self.SELLER

    @property
    def is_buyer(self):
        return self.role == self.BUYER

    @property
    def is_manager(self):
        return self.role == self.MANAGER

    @property
    def is_premium(self):
        return self.account_type == self.PREMIUM