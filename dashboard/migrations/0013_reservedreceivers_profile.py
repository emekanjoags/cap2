# Generated by Django 3.0.8 on 2020-09-13 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_auto_20200913_1504'),
        ('dashboard', '0012_reservedreceivers_have_received'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservedreceivers',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.Profile'),
        ),
    ]
