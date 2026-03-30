from django.urls import path
from .views import ModerateCarView, CarModerationLogsView, PendingCarsView

urlpatterns = [
    path('pending/', PendingCarsView.as_view(), name='pending-cars'),
    path('cars/<int:car_id>/moderate/', ModerateCarView.as_view(), name='moderate-car'),
    path('cars/<int:car_id>/logs/', CarModerationLogsView.as_view(), name='moderation-logs'),
]