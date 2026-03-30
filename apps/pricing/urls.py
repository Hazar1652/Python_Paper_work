from django.urls import path
from .views import CurrentRatesView, RefreshRatesView

urlpatterns = [
    path('rates/', CurrentRatesView.as_view(), name='current-rates'),
    path('rates/refresh/', RefreshRatesView.as_view(), name='refresh-rates'),
]