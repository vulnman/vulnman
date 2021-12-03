from rest_framework import serializers
from vulns import models


class VulnerabilityTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VulnerabilityTemplate
        fields = ['name', 'description', 'remediation', 'references', 'impact']
