from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, MeView

urlpatterns = [
    # POST /auth/register/ — створити акаунт
    path('register/', RegisterView.as_view(), name='auth-register'),

    # POST /auth/login/ — отримати JWT токен
    # Приймає username + password, повертає access + refresh токени
    path('login/', TokenObtainPairView.as_view(), name='auth-login'),

    # POST /auth/token/refresh/ — оновити токен коли він протух
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # GET/PUT /auth/me/ — мій профіль
    path('me/', MeView.as_view(), name='auth-me'),
]