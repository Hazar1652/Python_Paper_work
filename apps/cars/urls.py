from django.urls import path
from .views import CarListCreateView, CarDetailView, MakeListView, CarModelListView

urlpatterns = [
    # GET — список активних оголошень, POST — створити нове
    path('', CarListCreateView.as_view(), name='car-list-create'),

    # GET/PUT/DELETE — конкретне оголошення
    path('<int:pk>/', CarDetailView.as_view(), name='car-detail'),

    # Довідники марок і моделей
    path('makes/', MakeListView.as_view(), name='make-list'),
    path('makes/<int:make_id>/models/', CarModelListView.as_view(), name='model-list'),
]