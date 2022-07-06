from rest_framework import serializers
from vulnman.core.utils.markdown import md_to_clean_html
from apps.findings import models


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Template
        fields = [
            "uuid", "vulnerability_id", "cwe_ids", "name",
            "description", "recommendation", "category"]
        read_only_fields = ["uuid"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["description"] = md_to_clean_html(data["description"])
        return data
