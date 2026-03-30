from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from apps.cars.models import Car
from apps.cars.serializers import CarSerializer
from .services import moderate_car
from .models import ModerationLog
from rest_framework import serializers


class ModerationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationLog
        fields = ['id', 'car', 'status', 'flagged_words', 'comment', 'created_at']


class ModerateCarView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, car_id):
        if request.user.role not in ['manager', 'admin']:
            return Response(
                {'error': 'Тільки менеджери можуть модерувати оголошення'},
                status=403
            )

        result = moderate_car(car_id)
        return Response(result)


class CarModerationLogsView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, car_id):
        if request.user.role not in ['manager', 'admin']:
            return Response({'error': 'Доступ заборонено'}, status=403)

        logs = ModerationLog.objects.filter(car_id=car_id)
        serializer = ModerationLogSerializer(logs, many=True)
        return Response(serializer.data)


class PendingCarsView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role not in ['manager', 'admin']:
            return Response({'error': 'Доступ заборонено'}, status=403)

        pending_cars = Car.objects.filter(
            status__in=['pending', 'flagged']
        ).select_related('owner', 'make', 'model')

        serializer = CarSerializer(pending_cars, many=True)
        return Response(serializer.data)