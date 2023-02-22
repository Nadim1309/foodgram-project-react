from recipes.models import Ingredient
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from users.models import Follow, User
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator


class CustomAuthTokenSerializer(ModelSerializer):
    password = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User
        fields = ("email", "password")

    def validate(self, attrs):
        user = get_object_or_404(User, email=attrs["email"])
        if not user.check_password(attrs["password"]):
            raise serializers.ValidationError({"password": "Неверный пароль."})
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Функция проверяет подписан ли пользователь на объект"""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"
