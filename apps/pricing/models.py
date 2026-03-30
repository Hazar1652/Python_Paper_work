from django.db import models


class ExchangeRate(models.Model):
    # Зберігаємо курси валют кожного дня
    # Це важливо — якщо курс зміниться, старі оголошення
    # показуватимуть той курс який був на момент створення

    USD = 'USD'
    EUR = 'EUR'
    CURRENCY_CHOICES = [
        (USD, 'USD'),
        (EUR, 'EUR'),
    ]

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    # Скільки гривень коштує 1 USD або 1 EUR
    rate_to_uah = models.DecimalField(max_digits=10, decimal_places=4)

    # Дата коли був записаний цей курс
    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.currency} → UAH: {self.rate_to_uah} ({self.date})'

    class Meta:
        # Унікальна комбінація валюти і дати
        # Один курс USD на день, один курс EUR на день
        unique_together = ('currency', 'date')
        ordering = ['-date']