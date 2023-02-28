from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites_user',)
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites',)

    class Meta:
        ordering = ['-id']

        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_favorite')]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart',)
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='cart',)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Рецепты в корзине'
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_cart')]


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=180,)
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=20,)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Общий список ингредиентов'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_ingredient')]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=180,
        unique=True,)
    color = models.CharField(
        '"Цветовой HEX-код"',
        max_length=7,
        unique=True,)
    slug = models.SlugField(
        'Метка',
        unique=True,
        max_length=200,)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Список тегов'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',)
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=50,
        blank=False,)
    image = models.ImageField(
        'Картинка для рецепта',
        upload_to='resipes/',
        blank=False,)
    text = models.TextField(
        verbose_name='Описание рецепта',
        blank=False,)
    ingredients = models.ManyToManyField(
        'Ingredient',
        verbose_name='Ингредиенты',
        through='IngredientAmount',
        related_name='recipes',
        blank=False,)
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги',
        related_name='recipes',
        blank=False,)
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Время приготовления',
        validators=(
            MinValueValidator(
                1, message='Время приготовления не может быть меньше минуты'),),
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации рецепта',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Общий список рецептов'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.name}'


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='amount',
        verbose_name='В рецепте')
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.PROTECT,
        related_name='amount',
        verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество ингредиента',
        validators=(
            MinValueValidator(
                1, message='Количество не может быть меньше 1'),),
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов в рецепте'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique_ingredient_amount',
            ),
        )
