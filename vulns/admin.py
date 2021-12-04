from django.contrib import admin
from vulns import models


# Register your models here.
admin.site.register(models.Vulnerability)
admin.site.register(models.VulnerabilityTemplate)
admin.site.register(models.ProofOfConcept)
admin.site.register(models.WebApplicationUrlPath)
