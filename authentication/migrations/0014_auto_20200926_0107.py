# Generated by Django 3.0.8 on 2020-09-26 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_blockeduser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]