# Generated by Django 3.2.4 on 2021-07-07 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_alter_projectclassification_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectcontact',
            options={'verbose_name': 'Project Contact', 'verbose_name_plural': 'Project Contacts'},
        ),
        migrations.AddField(
            model_name='projectcontact',
            name='pgp_fingerprint',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]