from django.contrib import admin

from .models import Ingredient, IngredientAmount, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pub_date')
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags', 'pub_date',)
    ordering = ['pub_date', 'name',]
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ['name',]
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    search_fields = ('ingredient',)
    list_filter = ('ingredient',)
    ordering = ['ingredient',]
    empty_value_display = '-пусто-'
