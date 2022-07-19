# Generated by Django 4.0.6 on 2022-07-15 11:19

from django.db import migrations, models
import uuid

def migrate_uuids(apps, schema_editor):
    ImageProof = apps.get_model('responsible_disc', 'ImageProof')
    TextProof = apps.get_model('responsible_disc', 'TextProof')
    for proof in ImageProof.objects.all():
        proof.uuid = uuid.uuid4()
        proof.save()
    for proof in TextProof.objects.all():
        proof.uuid = uuid.uuid4()
        proof.save()


class Migration(migrations.Migration):

    dependencies = [
        ('responsible_disc', '0007_imageproof_uuid_textproof_uuid'),
    ]

    operations = [
        migrations.RunPython(migrate_uuids)
    ]