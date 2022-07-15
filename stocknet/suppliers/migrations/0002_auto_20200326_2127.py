# Generated by Django 2.2 on 2020-03-26 20:27

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='Type',
            field=models.CharField(choices=[(1, 'Particulier'), (2, 'Entreprise')], default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='supplier',
            name='Phone',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31),
        ),
    ]