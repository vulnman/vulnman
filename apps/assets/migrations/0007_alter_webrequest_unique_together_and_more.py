# Generated by Django 4.0.7 on 2022-08-25 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0006_weburl'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='webrequest',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='webrequest',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='webrequest',
            name='project',
        ),
        migrations.RemoveField(
            model_name='webrequest',
            name='web_app',
        ),
        migrations.RemoveField(
            model_name='weburl',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='weburl',
            name='project',
        ),
        migrations.RemoveField(
            model_name='weburl',
            name='webapp',
        ),
        migrations.AddField(
            model_name='service',
            name='accessibility',
            field=models.IntegerField(choices=[(1, 'Accessible'), (2, 'Not Accessible'), (0, 'Not Tested')], default=0),
        ),
        migrations.AddField(
            model_name='webapplication',
            name='accessibility',
            field=models.IntegerField(choices=[(1, 'Accessible'), (2, 'Not Accessible'), (0, 'Not Tested')], default=0),
        ),
    ]