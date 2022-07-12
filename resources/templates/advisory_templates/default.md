# {{ vulnerability.vendor }} {{ vulnerability.product }} - {{ vulnerability.template.name }}

{% if vulnerability.cve_id %}
**CVE-ID:** {{ vulnerability.cve_id }}
{% else %}
**CVE-ID:** -
{% endif %}

**Vendor:** [{{vulnerability.vendor}}]({{vulnerability.vendor_homepage}})

**Affected Product:** {{ vulnerability.affected_product }}

**Affected Versions:** {{ vulnerability.affected_versions|safe }}

**Vulnerability:** {{ vulnerability.template.name }}

**Status:** {{ vulnerability.get_status_display }}

**Severity:** {{ vulnerability.get_severity_display }}


## Timeline

{% for log in vulnerability.vulnerabilitylog_set.all %}
- {{ log.date_created|date }}: {{ log.get_action_display }}
{% endfor %}


## Details
{% for proof in vulnerability.proofs %}
{{ proof.description|safe }}

{% if proof.image %}
![{{ proof.image_as_basename }}]({{ proof.image_as_basename }})
{% else %}
{{ proof.text|safe }}
{% endif %}
{% endfor %}