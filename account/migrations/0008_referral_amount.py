# Generated by Django 3.0.8 on 2020-10-07 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_withrawrefbal_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]
