# Generated by Django 3.0.8 on 2020-08-27 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_remove_profile_has_referred'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='has_referred',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]