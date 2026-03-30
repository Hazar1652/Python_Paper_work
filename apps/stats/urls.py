from django.urls import path
from .views import CarStatsView, RecordViewPublicView

urlpatterns = [
    # Статистика для власника (Premium)
    path('<int:car_id>/', CarStatsView.as_view(), name='car-stats'),

    # Записати перегляд
    path('<int:car_id>/view/', RecordViewPublicView.as_view(), name='record-view'),
]