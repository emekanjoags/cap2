# Generated by Django 3.0.8 on 2020-10-07 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_referral_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
