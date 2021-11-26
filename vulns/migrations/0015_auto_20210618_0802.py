# Generated by Django 3.2.4 on 2021-06-18 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0014_auto_20210618_0630'),
        ('vulns', '0014_vulnerability_cvss_base_score'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vulnerability',
            options={'ordering': ['-cvss_base_score']},
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='cvss_string',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='CVSS Vector'),
        ),
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
