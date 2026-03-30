from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .services import record_view, get_view_stats, get_price_stats
from apps.cars.models import Car


class CarStatsView(APIView):
    """
    GET /stats/<car_id>/
    Повертає статистику для Premium користувачів.
    Також записує перегляд для всіх користувачів.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, car_id):
        # Перевіряємо що оголошення існує
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({'error': 'Оголошення не знайдено'}, status=404)

        # Записуємо перегляд для всіх
        record_view(car_id)

        # Статистику показуємо тільки Premium користувачам
        # і тільки власнику оголошення
        if car.owner != request.user:
            return Response({'error': 'Статистика доступна тільки власнику'}, status=403)

        if request.user.account_type != 'premium':
            return Response({
                'error': 'Статистика доступна тільки для Premium акаунтів',
                'upgrade_url': '/pricing/upgrade/'
            }, status=403)

        # Збираємо всю статистику
        view_stats = get_view_stats(car_id)
        price_stats = get_price_stats(car_id)

        return Response({
            'car_id': car_id,
            'views': view_stats,
            'pricing': price_stats,
        })


class RecordViewPublicView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, car_id):
        record_view(car_id)
        return Response({'recorded': True})