# Generated by Django 3.2.9 on 2021-12-09 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_delete_commandhistoryitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectmember',
            options={'ordering': ['-user__username']},
        ),
    ]