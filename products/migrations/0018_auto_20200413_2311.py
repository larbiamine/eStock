# Generated by Django 2.2 on 2020-04-13 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_stocktrack_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='SalesPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
