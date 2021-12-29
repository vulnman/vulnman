# Customize Report

## Change Report Template
Change the `REPORT_TEMPLATE` setting in your [settings file](../../getting_started/configuration/index.md).

## HTML Reports
HTML reports can contain Markdown sections. These can be customized by providing a markdown file in the `REPORT_SECTIONS`
setting.

An example can be found below:
```python
REPORT_SECTIONS = [
    {"title": "Cover", "template": os.path.join(REPORT_TEMPLATE_CHAPTERS_DIR, "cover.html"), "content": None},
    {"title": "Assessment Information",
     "template": os.path.join(REPORT_TEMPLATE_CHAPTERS_DIR, "assessment_information.html"),
     "content": None},
    {"title": "Assessment Overview", "template": os.path.join(REPORT_TEMPLATE_CHAPTERS_DIR, "generic_md_section.html"),
     "content": "default.md"},
    {"title": "Methodology", "template": os.path.join(REPORT_TEMPLATE_CHAPTERS_DIR, "generic_md_section.html"),
     "content": "default.md"},
    {"title": "Vulnerability Overview",
     "template": os.path.join(REPORT_TEMPLATE_CHAPTERS_DIR, "vulnerability_overview.html"),
     "content": None},
    {"title": "Vulnerability Listing",
     "template": os.path.join(REPORT_TEMPLATE_CHAPTERS_DIR, "vulnerability_listing.html"),
     "content": None}
]
```

You can even use [django's template language](https://docs.djangoproject.com/en/4.0/ref/templates/language/)
inside your markdown files.

This will only be rendered on initial report creation and will not be used on report editing to prevent 
[SSTI](https://portswigger.net/research/server-side-template-injection)
vulnerabilities.


## LaTeX Reports

!!! warning
    LaTeX reports will be deprecated in 0.2.2


### Report Assets
If you need to include custom graphics into your report, you should add them to the `templates/custom/report/assets` directory.

Proof of concept files are included by default.
