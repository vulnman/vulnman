# Vulnerability Templates

Vulnman allows you to create vulnerabilities based on templates.


## Import CWE Database
You can import CWE database by downloading the [CWE XML](https://cwe.mitre.org/data/downloads.html)
and pass the file to the `import_cwe` management command.

```
python manage.py import_cwe cwec_v4.4.xml
```
