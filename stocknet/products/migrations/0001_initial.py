# Generated by Django 2.2 on 2020-03-16 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.TextField()),
                ('Description', models.TextField()),
                ('PurchasePrice', models.TextField()),
                ('SalesPrice', models.TextField()),
                ('Reference', models.TextField()),
                ('Manufacturer', models.TextField()),
                ('Category', models.TextField()),
                ('Quantity', models.TextField()),
            ],
        ),
    ]