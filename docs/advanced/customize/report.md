# Customize Report

## Change Report Theme
Change the `REPORT_TEMPLATE` setting in your [settings file](../../getting_started/configuration).

## HTML Reports
You can customize the default texts for some sections.
Just create markdown file with the content and change the following settings.

```python
CUSTOM_REPORT_SECTIONS = {
    "methodology": "/storage/reporting/sections/methodology.md
}
```

## LaTeX Reports

### Report Assets
If you need to include custom graphics into your report, you should add them to the `templates/custom/report/assets` directory.

Proof of concept files are included by default.
