# Generated by Django 4.1.2 on 2022-11-14 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_alter_customerprofile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_role',
            field=models.PositiveIntegerField(choices=[(0, 'Pentester'), (2, 'Customer'), (1, 'Vendor'), (3, 'Bughunter')], null=True),
        ),
    ]
