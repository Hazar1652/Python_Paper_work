from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    # write_only=True — пароль приймаємо але ніколи не повертаємо у відповіді
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]  # перевіряє мінімальну довжину тощо
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'role', 'phone']

    def validate(self, attrs):
        # Перевіряємо що обидва паролі однакові
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Паролі не співпадають'})
        return attrs

    def create(self, validated_data):
        # Видаляємо password2 — він нам більше не потрібен
        validated_data.pop('password2')
        password = validated_data.pop('password')

        # Створюємо користувача
        user = CustomUser(**validated_data)

        # set_password хешує пароль перед збереженням
        # Ніколи не зберігай пароль як звичайний текст!
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    # Цей серіалізатор для читання даних користувача
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'account_type', 'phone', 'is_verified']
        # read_only_fields — ці поля не можна змінити через API
        read_only_fields = ['id', 'account_type', 'is_verified']