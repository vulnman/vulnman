# Generated by Django 4.0.5 on 2022-07-01 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0012_report_task_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='task_id',
        ),
        migrations.AddField(
            model_name='report',
            name='work_in_progress',
            field=models.BooleanField(default=False),
        ),
    ]
