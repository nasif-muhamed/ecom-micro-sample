# Generated by Django 5.1.4 on 2024-12-29 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product_name',
        ),
        migrations.AddField(
            model_name='order',
            name='product_id',
            field=models.IntegerField(default=2, max_length=255),
            preserve_default=False,
        ),
    ]
