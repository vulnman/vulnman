# Generated by Django 4.0.5 on 2022-07-01 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0013_remove_report_task_id_report_work_in_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='work_in_progress',
        ),
        migrations.AddField(
            model_name='reportrelease',
            name='work_in_progress',
            field=models.BooleanField(default=False),
        ),
    ]
