from rest_framework import serializers
from apps.findings import models
from vulnman.core.utils.markdown import md_to_clean_html


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
