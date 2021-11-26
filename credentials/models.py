from django.db import models
from uuid import uuid4


# Create your models here.
class Credentials(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid4)
	username = models.CharField(max_length=128)
	cleartext_password = models.CharField(max_length=255)
	hashed_password = models.CharField(max_length=512)
	location_found = models.CharField(max_length=512)
	project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
