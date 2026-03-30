from rest_framework import serializers
from .models import Car, Make, CarModel


class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['id', 'name']


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'make']


class CarSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    make_name = serializers.CharField(source='make.name', read_only=True)
    model_name = serializers.CharField(source='model.name', read_only=True)

    class Meta:
        model = Car
        fields = [
            'id', 'owner_username', 'make', 'make_name',
            'model', 'model_name', 'year', 'mileage',
            'description', 'price', 'currency',
            'price_usd', 'price_eur', 'price_uah',
            'city', 'region', 'status', 'edit_count',
            'image', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'owner_username', 'make_name', 'model_name',
            'price_usd', 'price_eur', 'price_uah',
            'exchange_rate_used', 'status', 'edit_count',
            'created_at', 'updated_at'
        ]

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user

        if not self.instance:  # тільки при створенні (не при оновленні)
            if user.account_type == 'basic':
                active_cars = Car.objects.filter(
                    owner=user,
                    status__in=['active', 'pending']
                ).count()
                if active_cars >= 1:
                    raise serializers.ValidationError(
                        'Basic акаунт може мати тільки 1 активне оголошення. '
                        'Оновіться до Premium для необмеженої кількості.'
                    )
        return attrs