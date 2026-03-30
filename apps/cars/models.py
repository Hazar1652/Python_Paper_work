from django.db import models
from django.conf import settings


class Make(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.make.name} {self.name}'

    class Meta:
        unique_together = ('make', 'name')


class Car(models.Model):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    FLAGGED = 'flagged'
    PENDING = 'pending'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (FLAGGED, 'Flagged'),
        (PENDING, 'Pending moderation'),
    ]

    # Валюти
    USD = 'USD'
    EUR = 'EUR'
    UAH = 'UAH'
    CURRENCY_CHOICES = [
        (USD, 'USD'),
        (EUR, 'EUR'),
        (UAH, 'UAH'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cars'
    )

    make = models.ForeignKey(Make, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True)

    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=USD)

    # Ціни в інших валютах — розраховуються автоматично
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_eur = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_uah = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    exchange_rate_used = models.DecimalField(
        max_digits=10, decimal_places=4,
        null=True, blank=True
    )

    city = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    edit_count = models.PositiveIntegerField(default=0)  # лічильник редагувань

    image = models.ImageField(upload_to='cars/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.make} {self.model} {self.year} — {self.owner.username}'

    class Meta:
        ordering = ['-created_at']