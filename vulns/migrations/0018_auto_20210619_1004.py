# Generated by Django 3.2.4 on 2021-06-19 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vulns', '0017_vulnerabilitytemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='references',
            field=models.CharField(help_text='comma separated list of references', max_length=64),
        ),
    ]
