# Generated by Django 3.2 on 2024-04-13 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_order_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderaddress',
            name='address1',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='orderaddress',
            name='address2',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='orderaddress',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='orderaddress',
            name='country',
            field=models.CharField(max_length=30),
        ),
    ]
