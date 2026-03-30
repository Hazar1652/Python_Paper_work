from django.db import models


class ExchangeRate(models.Model):
    USD = 'USD'
    EUR = 'EUR'
    CURRENCY_CHOICES = [
        (USD, 'USD'),
        (EUR, 'EUR'),
    ]

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    rate_to_uah = models.DecimalField(max_digits=10, decimal_places=4)

    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.currency} → UAH: {self.rate_to_uah} ({self.date})'

    class Meta:
        unique_together = ('currency', 'date')
        ordering = ['-date']