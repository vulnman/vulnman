# Generated by Django 4.1.2 on 2022-10-08 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_customerprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='position',
            field=models.CharField(default='unknown', max_length=64),
        ),
    ]
