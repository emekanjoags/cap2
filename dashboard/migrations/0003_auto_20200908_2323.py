# Generated by Django 3.0.8 on 2020-09-08 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_receivers_enter_list'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='receivers',
            options={'verbose_name_plural': 'Receivers'},
        ),
        migrations.RenameField(
            model_name='makedonation',
            old_name='name',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='receivers',
            old_name='name',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='receiverslist',
            old_name='name',
            new_name='user',
        ),
    ]
