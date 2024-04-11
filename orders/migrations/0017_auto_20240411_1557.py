# Generated by Django 3.2 on 2024-04-11 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_alter_order_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_default',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
