# Generated by Django 3.0.8 on 2020-09-08 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_receivers_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receivers',
            name='profile',
        ),
        migrations.AddField(
            model_name='receivers',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
