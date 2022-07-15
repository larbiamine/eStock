# Generated by Django 2.2 on 2020-03-26 20:49

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_suppliers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Suppliers',
        ),
        migrations.AddField(
            model_name='product',
            name='Suppliers',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Particulier', 'Particulier'), ('Entreprise', 'Entreprise')], default=0, max_length=22),
            preserve_default=False,
        ),
    ]
