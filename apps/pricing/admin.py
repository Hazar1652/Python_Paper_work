from django.contrib import admin
from .models import ExchangeRate


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['currency', 'rate_to_uah', 'date', 'created_at']
    list_filter = ['currency']
    ordering = ['-date']