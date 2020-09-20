# Generated by Django 3.0.8 on 2020-08-26 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20200826_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='has_withdrawn',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_referred',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='referral_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]