# Generated by Django 3.2.18 on 2023-03-01 16:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные рецепты',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=180, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(max_length=20, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Общий список ингредиентов',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Количество не может быть меньше 1')], verbose_name='Количество ингредиента')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='amount', to='recipes.ingredient', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Количество ингредиента',
                'verbose_name_plural': 'Количество ингредиентов в рецепте',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название рецепта')),
                ('image', models.ImageField(upload_to='resipes/', verbose_name='Картинка для рецепта')),
                ('text', models.TextField(verbose_name='Описание рецепта')),
                ('cooking_time', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Время приготовления не может быть меньше минуты')], verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации рецепта')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(related_name='recipes', through='recipes.IngredientAmount', to='recipes.Ingredient', verbose_name='Ингредиенты')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Общий список рецептов',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=180, unique=True, verbose_name='Название')),
                ('color', models.CharField(max_length=7, unique=True, verbose_name='"Цветовой HEX-код"')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Метка')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Список тегов',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='recipes.recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Рецепты в корзине',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount', to='recipes.recipe', verbose_name='В рецепте'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingredient'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_cart'),
        ),
        migrations.AddConstraint(
            model_name='ingredientamount',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_ingredient_amount'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite'),
        ),
    ]
