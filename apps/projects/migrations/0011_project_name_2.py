from django.db import migrations, models


def migrate_names(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    for obj in Project.objects.all():
        obj.name = obj.client.name
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_alter_clientcontact_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.RunPython(migrate_names),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=128, null=False),
        ),
    ]
