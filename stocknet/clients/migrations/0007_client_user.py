# Generated by Django 2.2 on 2020-03-30 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0006_auto_20200326_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clientlist', to=settings.AUTH_USER_MODEL),
        ),
    ]