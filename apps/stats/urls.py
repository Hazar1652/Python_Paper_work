from django.urls import path
from .views import CarStatsView, RecordViewPublicView

urlpatterns = [
    path('<int:car_id>/', CarStatsView.as_view(), name='car-stats'),

    path('<int:car_id>/view/', RecordViewPublicView.as_view(), name='record-view'),
]