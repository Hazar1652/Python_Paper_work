from django.urls import path
from .views import CarListCreateView, CarDetailView, MakeListView, CarModelListView

urlpatterns = [
    path('', CarListCreateView.as_view(), name='car-list-create'),
    path('<int:pk>/', CarDetailView.as_view(), name='car-detail'),
    path('makes/', MakeListView.as_view(), name='make-list'),
    path('makes/<int:make_id>/models/', CarModelListView.as_view(), name='model-list'),
]