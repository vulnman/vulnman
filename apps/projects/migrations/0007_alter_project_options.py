# Generated by Django 3.2.9 on 2021-12-23 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20211219_1518'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-date_updated'], 'permissions': [('pentest_project', 'Pentest Project')]},
        ),
    ]