# Generated by Django 4.0.6 on 2022-07-07 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectapitoken',
            options={'ordering': ['-date_valid']},
        ),
        migrations.AlterModelOptions(
            name='projectcontributor',
            options={'ordering': ['-date_created']},
        ),
    ]
