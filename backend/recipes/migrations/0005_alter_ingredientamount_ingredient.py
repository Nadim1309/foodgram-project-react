# Generated by Django 4.1.7 on 2023-02-25 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_ingredientamount_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ingradient', to='recipes.ingredient', verbose_name='Ингредиент'),
        ),
    ]
