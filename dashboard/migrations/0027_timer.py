# Generated by Django 3.0.8 on 2020-09-21 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0026_receivers_has_entered_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_appear', models.DateField()),
                ('list_disappear', models.DateField()),
            ],
        ),
    ]