# Generated by Django 5.1.1 on 2024-10-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_description_alter_product_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='რაოდენობა'),
        ),
    ]
