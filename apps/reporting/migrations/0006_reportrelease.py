# Generated by Django 4.0.5 on 2022-06-29 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
        ('reporting', '0005_report_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportRelease',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('release_type', models.CharField(choices=[('draft', 'Draft'), ('release', 'Release')], max_length=16)),
                ('raw_source', models.TextField()),
                ('compiled_source', models.BinaryField(blank=True, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.report')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
