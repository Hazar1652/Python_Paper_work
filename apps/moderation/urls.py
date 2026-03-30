from django.urls import path
from .views import ModerateCarView, CarModerationLogsView, PendingCarsView

urlpatterns = [
    # Список оголошень що чекають модерації
    path('pending/', PendingCarsView.as_view(), name='pending-cars'),

    # Запустити модерацію для конкретного оголошення
    path('cars/<int:car_id>/moderate/', ModerateCarView.as_view(), name='moderate-car'),

    # Історія модерації оголошення
    path('cars/<int:car_id>/logs/', CarModerationLogsView.as_view(), name='moderation-logs'),
]