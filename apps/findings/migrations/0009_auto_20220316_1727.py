# Generated by Django 3.2.12 on 2022-03-16 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('findings', '0008_vulnerability_severity'),
    ]

    operations = [
        migrations.AddField(
            model_name='vulnerability',
            name='auth_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vulnerability',
            name='user_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='findings.useraccount'),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='asset_type',
            field=models.CharField(choices=[('webapplication', 'Web Application'), ('webrequest', 'Web Request'), ('host', 'Host')], default='webapplication', max_length=64),
        ),
    ]
