# Generated by Django 3.2 on 2024-03-30 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20240329_1837'),
        ('orders', '0011_auto_20240323_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='products.product'),
        ),
    ]
