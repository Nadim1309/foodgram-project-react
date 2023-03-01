import json
from django.db import migrations
from django.db import transaction


@transaction.atomic
def add_tags(apps, shema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    with open('../data/tags.json', encoding='utf-8') as t:
        tags = json.load(t)
    for tag in range(len(tags)):
        Tag.objects.create(name=tags[tag]['name'], color=tags[tag]
                           ['color'], slug=tags[tag]['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [migrations.RunPython(add_tags),]
