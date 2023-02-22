from django.http import HttpResponse
from recipes.models import Ingredient
from rest_framework import filters, generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from backend.users.models import User

from .serializers import CustomAuthTokenSerializer, IngredientSerializer


class IngredientList(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all
    serializer_class = IngredientSerializer


@api_view(["POST"])
def get_token(request):
    serializer = CustomAuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(email=request.data["email"])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"auth_token": token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def del_token(request):
    token, _ = Token.objects.get_or_create(user=request.user)
    token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
