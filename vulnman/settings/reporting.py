# Reporting
REPORT_COMPANY_INFORMATION = {
    "name": "Vulnman",
    "street": "No Street 54",
    "zip": "123456 Berlin",
    "country": "Germany",
    "homepage": "https://vulnman.github.io",
    "contact": "contact@example.com"
}

REPORTING_TEMPLATE = "vulnman.report_templates.default.DefaultReportTemplate"
CELERY_RESULT_BACKEND = 'django-db'


# Report Templates
REPORT_TEMPLATES = {
    "default": {
        "CSS": ["report.css", "fontawesome.min.css"]
    }
}
