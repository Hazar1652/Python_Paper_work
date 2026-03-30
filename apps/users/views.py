from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from .models import CustomUser


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    # AllowAny — цей endpoint доступний без авторизації
    # Бо як інакше зареєструватись якщо ще немає токена? :)
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    # Повертає або оновлює дані поточного користувача
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Повертаємо самого себе — того хто робить запит
        return self.request.user