# Generated by Django 3.0.8 on 2020-09-17 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_auto_20200918_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='receivers',
            name='date_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
