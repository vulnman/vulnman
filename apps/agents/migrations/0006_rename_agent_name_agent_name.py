# Generated by Django 3.2.9 on 2021-12-07 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0005_agentqueue_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agent',
            old_name='agent_name',
            new_name='name',
        ),
    ]