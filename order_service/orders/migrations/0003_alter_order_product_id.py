# Generated by Django 5.0.6 on 2024-12-31 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_product_name_order_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_id',
            field=models.IntegerField(),
        ),
    ]
