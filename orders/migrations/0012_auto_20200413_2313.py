# Generated by Django 2.2 on 2020-04-13 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20200411_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientorder',
            name='Total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='supplierorder',
            name='Total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True),
        ),
    ]