# Generated by Django 2.2 on 2020-03-30 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0007_auto_20200328_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todolist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='Suppliers',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('HP', 'HP'), ('azdazd', 'azdazd'), ('hesgbhke', 'hesgbhke'), ('afaefzf', 'afaefzf'), ('LG', 'LG'), ('Sony', 'Sony'), ('Asus', 'Asus'), ('Acer', 'Acer'), ('Dell', 'Dell')], max_length=49),
        ),
    ]
