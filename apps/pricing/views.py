from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .services import fetch_rates_from_privatbank, get_today_rates


class CurrentRatesView(APIView):
    # Показує поточні курси валют — доступно всім
    permission_classes = [AllowAny]

    def get(self, request):
        rates = get_today_rates()
        return Response({
            'USD_to_UAH': rates.get('USD'),
            'EUR_to_UAH': rates.get('EUR'),
        })


class RefreshRatesView(APIView):
    # Оновлює курси вручну — тільки для адміна
    def get(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Тільки для адміністраторів'}, status=403)
        rates = fetch_rates_from_privatbank()
        return Response({'message': 'Курси оновлено', 'rates': {
            k: str(v) for k, v in rates.items()
        }})