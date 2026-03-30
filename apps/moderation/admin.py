from django.contrib import admin
from .models import ModerationLog


@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'car', 'status', 'flagged_words', 'checked_by', 'created_at']
    list_filter = ['status']
    ordering = ['-created_at']