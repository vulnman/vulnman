# Generated by Django 3.2.9 on 2021-11-29 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vulns', '0039_webapplication_webapplicationurlpath'),
    ]

    operations = [
        migrations.AddField(
            model_name='webapplicationurlpath',
            name='webapp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vulns.webapplication'),
        ),
    ]