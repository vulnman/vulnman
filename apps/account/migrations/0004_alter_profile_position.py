# Generated by Django 3.2.4 on 2021-06-16 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='position',
            field=models.CharField(default='Pentester', help_text='Position mentioned in report', max_length=32),
        ),
    ]