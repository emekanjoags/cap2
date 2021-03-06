# Generated by Django 3.0.8 on 2020-09-12 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0009_auto_20200912_0102'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountDonated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('receiver_created', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
