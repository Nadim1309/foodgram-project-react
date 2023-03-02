from api.filters import IngredientSearchFilter, RecipeFilter
from api.permissions import AdminOrReadOnly, AdminUserOrReadOnly
from django.db.models import BooleanField, Exists, OuterRef, Value
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import *
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from users.models import Follow

from .serializers import *

User = get_user_model()


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [AdminUserOrReadOnly,]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.all()

        if user.is_authenticated:
            queryset = queryset.annotate(
                is_favorited=Exists(Favorite.objects.filter(
                    user=user, recipe__pk=OuterRef('pk'))
                ),
                is_in_shopping_cart=Exists(ShoppingCart.objects.filter(
                    user=user, recipe__pk=OuterRef('pk'))
                )
            )
        else:
            queryset = queryset.annotate(
                is_favorited=Value(False, output_field=BooleanField()),
                is_in_shopping_cart=Value(False, output_field=BooleanField())
            )
        return queryset

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return self.add_obj(Favorite, request.user, pk)

    @favorite.mapping.delete
    def del_from_favorite(self, request, pk=None):
        return self.delete_obj(Favorite, request.user, pk)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self.add_obj(ShoppingCart, request.user, pk)

    @shopping_cart.mapping.delete
    def del_from_shopping_cart(self, request, pk=None):
        return self.delete_obj(ShoppingCart, request.user, pk)

    def add_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                'errors': 'Ошибка добавления рецепта в список'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Ошибка удаления рецепта из списка'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_dict = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        for item in ingredients:
            name = item[0]
            if name not in shopping_dict:
                shopping_dict[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                shopping_dict[name]['amount'] += item[2]
        shopping_list = []
        for index, key in enumerate(shopping_dict, start=1):
            shopping_list.append(
                f'{index}. {key} - {shopping_dict[key]["amount"]} '
                f'{shopping_dict[key]["measurement_unit"]}\n')
        filename = 'shopping_cart.txt'

        file = open(filename, 'w', encoding='utf-8')
        for key, value in shopping_dict.items():
            file.write(
                f'{index}. {key} - {shopping_dict[key]["amount"]} '
                f'{shopping_dict[key]["measurement_unit"]}\n')
        file.close()

        response = HttpResponse(shopping_list,
                                content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class FollowViewSet(UserViewSet):
    pagination_class = CustomPageNumberPagination

    @ action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if user == author:
                return Response({
                    'errors': 'Нельзя подписываться на себя'
                }, status=status.HTTP_400_BAD_REQUEST)
            if Follow.objects.filter(user=user, author=author).exists():
                return Response({
                    'errors': 'Вы уже подписаны на пользователя'
                }, status=status.HTTP_400_BAD_REQUEST)

            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                follow, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if user == author:
                return Response({
                    'errors': 'Нельзя отписываться от самого себя'
                }, status=status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.filter(user=user, author=author)
            if not follow.exists():
                return Response({
                    'errors': 'Вы уже отписались'
                }, status=status.HTTP_400_BAD_REQUEST)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @ action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)
