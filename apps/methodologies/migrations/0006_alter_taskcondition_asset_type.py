# Generated by Django 4.1.2 on 2022-10-21 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('methodologies', '0005_alter_taskcondition_asset_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcondition',
            name='asset_type',
            field=models.CharField(choices=[('webapplication', 'Web Application'), ('host', 'Host'), ('service', 'Service'), ('network', 'Network'), ('thickclient', 'Thick-Client')], max_length=128),
        ),
    ]