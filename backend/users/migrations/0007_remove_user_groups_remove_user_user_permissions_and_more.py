# Generated by Django 4.1.7 on 2023-02-23 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_is_admin_alter_user_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ['-id'], 'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique follow',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_follow'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
