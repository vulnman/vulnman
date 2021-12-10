# Generated by Django 3.2.9 on 2021-12-09 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networking', '0003_auto_20211209_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['-date_updated'], 'verbose_name': 'Service', 'verbose_name_plural': 'Services'},
        ),
        migrations.AlterUniqueTogether(
            name='service',
            unique_together={('host', 'port', 'protocol')},
        ),
    ]