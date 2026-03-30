from django.contrib import admin
from .models import Car, Make, CarModel


@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'make']
    list_filter = ['make']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'make', 'model', 'year', 'price', 'currency', 'status', 'owner']
    list_filter = ['status', 'currency', 'make']
    search_fields = ['description', 'owner__username']