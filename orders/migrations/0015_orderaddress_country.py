# Generated by Django 3.2 on 2024-04-08 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_orderaddress_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderaddress',
            name='country',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
