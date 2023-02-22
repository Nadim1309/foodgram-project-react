from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.CharField(
        error_messages={
            'unique': 'Пользователь с такой почтой уже зарегистрирован',
        },
        verbose_name='email',
        max_length=100,
        unique=True)

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50)

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50)

    username = models.CharField(
        error_messages={'unique': 'Этот никнейм занят', },
        max_length=30,
        unique=True,
        verbose_name='Никнейм'
    )

    def recipes_count(self):
        return self.recipes.all().count()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique follow',
            )
        ]
