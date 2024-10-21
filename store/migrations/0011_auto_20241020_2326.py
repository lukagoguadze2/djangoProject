# Generated by Django 5.1.1 on 2024-10-20 19:26

from django.db import migrations
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    cat = apps.get_model('store', 'Category')
    for category in cat.objects.all():
        category.slug = slugify(category.name)
        category.save()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_product_quantity'),
    ]

    operations = [
        migrations.RunPython(populate_slugs),
    ]
