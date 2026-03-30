from django.db import models
from django.conf import settings


class ModerationLog(models.Model):
    # Статуси перевірки
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    # Яке оголошення перевірялось
    car = models.ForeignKey(
        'cars.Car',
        on_delete=models.CASCADE,
        related_name='moderation_logs'
    )

    # Хто перевіряв (None = автоматична перевірка)
    checked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moderation_actions'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    # Які слова були знайдені
    flagged_words = models.TextField(blank=True)

    # Коментар менеджера
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Moderation #{self.id} — Car #{self.car_id} — {self.status}'

    class Meta:
        ordering = ['-created_at']