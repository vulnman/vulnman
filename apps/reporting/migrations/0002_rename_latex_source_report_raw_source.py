# Generated by Django 3.2.9 on 2021-12-03 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='latex_source',
            new_name='raw_source',
        ),
    ]
