# Generated by Django 4.0.5 on 2022-06-23 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_pentesterprofile_public_email_address_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InviteCode',
        ),
    ]
