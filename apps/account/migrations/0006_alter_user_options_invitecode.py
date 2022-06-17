# Generated by Django 4.0.5 on 2022-06-17 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_is_vendor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('invite_vendor', 'Invite Vendor')]},
        ),
        migrations.CreateModel(
            name='InviteCode',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254)),
                ('token', models.CharField(max_length=512)),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
