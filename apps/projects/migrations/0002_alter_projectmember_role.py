# Generated by Django 3.2.9 on 2021-12-05 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmember',
            name='role',
            field=models.CharField(choices=[('pentester', 'Pentester'), ('read-only', 'Read-Only')], max_length=16),
        ),
    ]
