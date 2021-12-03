# Generated by Django 3.2.9 on 2021-12-03 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_rename_latex_source_report_raw_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='report_language',
            field=models.CharField(choices=[('markdown', 'markdown'), ('latex', 'latex')], default='latex', max_length=16),
        ),
    ]
