# Generated by Django 3.2.9 on 2021-12-07 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_rename_parsed_command_commandhistoryitem_command'),
        ('agents', '0004_remove_agentqueue_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentqueue',
            name='project',
            field=models.ForeignKey(default='4cfbd79e-649f-4e86-84c9-cf9fa343e92f', on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
            preserve_default=False,
        ),
    ]
