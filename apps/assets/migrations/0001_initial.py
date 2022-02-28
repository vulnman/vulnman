<<<<<<< HEAD
# Generated by Django 3.2.10 on 2022-01-29 12:42
=======
# Generated by Django 3.2.12 on 2022-02-23 16:27
>>>>>>> origin/dev

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        ('commands', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0010_alter_clientcontact_options'),
=======
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
>>>>>>> origin/dev
    ]

    operations = [
        migrations.CreateModel(
            name='WebApplication',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True)),
                ('in_pentest_report', models.BooleanField(blank=True, default=True)),
                ('name', models.CharField(max_length=256)),
                ('base_url', models.URLField()),
<<<<<<< HEAD
                ('command_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commands.commandhistoryitem')),
=======
>>>>>>> origin/dev
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
            options={
<<<<<<< HEAD
                'abstract': False,
=======
                'verbose_name': 'Web Application',
                'verbose_name_plural': 'Web Applications',
>>>>>>> origin/dev
            },
        ),
        migrations.CreateModel(
            name='WebRequest',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True)),
                ('in_pentest_report', models.BooleanField(blank=True, default=True)),
                ('url', models.URLField(blank=True)),
                ('parameter', models.CharField(blank=True, max_length=255)),
<<<<<<< HEAD
                ('command_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commands.commandhistoryitem')),
=======
>>>>>>> origin/dev
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('web_app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.webapplication')),
            ],
            options={
<<<<<<< HEAD
                'abstract': False,
=======
                'verbose_name': 'Web Request',
                'verbose_name_plural': 'Web Requests',
                'unique_together': {('web_app', 'url', 'parameter')},
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('in_pentest_report', models.BooleanField(blank=True, default=True)),
                ('ip', models.GenericIPAddressField()),
                ('operating_system', models.CharField(blank=True, max_length=256)),
                ('accessibility', models.IntegerField(choices=[(1, 'Accessible'), (2, 'Not Accessible'), (0, 'Not Tested')], default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('dns', models.CharField(blank=True, max_length=256, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
            options={
                'ordering': ['ip'],
                'unique_together': {('project', 'ip')},
>>>>>>> origin/dev
            },
        ),
    ]
