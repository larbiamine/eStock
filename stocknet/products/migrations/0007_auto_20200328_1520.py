# Generated by Django 2.2 on 2020-03-28 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200328_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Description',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
