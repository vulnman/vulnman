# Customize Report

## Change Report Template
Change the `REPORTING_TEMPLATE` setting in your [settings file](../../getting_started/configuration/index.md).

## HTML Reports

You can create your own HTML report templates following this tutorial.

First create the directory for the template:

```bash
mkdir custom/report_templates/my_template
```

Create the following directories in there:
- contents
- sections

The main report file is called `report.html` and needs to be created inside your template directory.

Next, create the report python class in `custom/report_templates/my_template.py` with the following example content:

```python
import os
from django.conf import settings
from apps.reporting.utils.report_template import ReportSection, ReportTemplate


class MyReportTemplate(ReportTemplate):
    name = "my-html-template"
    template_directory = os.path.join(settings.BASE_DIR, "custom/report_templates/my_template")
    sections = [
        ReportSection("Cover", "cover.html", None),
        ReportSection("Methodology", "generic_md_section.html", "default.md"),
        ReportSection("Vulnerability Overview", "vulnerability_overview.html", None),
        ReportSection("Vulnerability Listing", "vulnerability_listing.html", None)
    ]
    stylesheets = [
        "report.css"
    ]
```

If you want to use CSS stylesheets, create the `report.css` file inside your template directory.

### Misc

HTML reports can contain Markdown sections.

You can even use [django's template language](https://docs.djangoproject.com/en/4.0/ref/templates/language/)
inside your markdown files.

This will only be rendered on initial report creation and will not be used on report editing to prevent 
[SSTI](https://portswigger.net/research/server-side-template-injection)
vulnerabilities.
