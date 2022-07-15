# Generated by Django 2.2 on 2020-04-11 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_stocktrack_user'),
        ('orders', '0010_clientorder_orders'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientorder',
            old_name='Total',
            new_name='Quantity',
        ),
        migrations.RenameField(
            model_name='supplierorder',
            old_name='Total',
            new_name='Quantity',
        ),
        migrations.RemoveField(
            model_name='clientorder',
            name='Orders',
        ),
        migrations.RemoveField(
            model_name='supplierorder',
            name='Orders',
        ),
        migrations.AddField(
            model_name='clientorder',
            name='Product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clientorderlist', to='products.Product'),
        ),
        migrations.AddField(
            model_name='supplierorder',
            name='Product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplierorderlist', to='products.Product'),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
