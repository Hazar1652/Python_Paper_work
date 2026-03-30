from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Додаємо наші поля до стандартного відображення
    list_display = ['username', 'email', 'role', 'account_type', 'is_verified']
    list_filter = ['role', 'account_type', 'is_verified']

    # Додаємо наші поля до форми редагування
    fieldsets = UserAdmin.fieldsets + (
        ('AutoRia Fields', {
            'fields': ('phone', 'role', 'account_type', 'is_verified')
        }),
    )