# Generated by Django 3.2.23 on 2024-02-11 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20240211_1714'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitems',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='session_key',
        ),
    ]
