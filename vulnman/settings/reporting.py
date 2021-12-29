import os
from vulnman.settings import BASE_DIR

# Reporting
REPORT_COMPANY_INFORMATION = {
    "name": "Vulnman",
    "street": "No Street 54",
    "zip": "123456 Berlin, Germany",
    "homepage": "https://vulnman.github.io/vulnman",
    "contact": "contact@example.com"
}

REPORT_TEMPLATE_DIR = "report/html_default"
REPORT_TEMPLATE_FULL_PATH = os.path.join(BASE_DIR, "apps/reporting/templates/%s" % REPORT_TEMPLATE_DIR)
REPORT_TEMPLATE_CHAPTERS_DIR = os.path.join(REPORT_TEMPLATE_DIR, "chapters/")
REPORT_TEMPLATE_CONTENTS_DIR = os.path.join(REPORT_TEMPLATE_FULL_PATH, "contents/")
REPORT_TEMPLATE = os.path.join(REPORT_TEMPLATE_DIR, "report.html")

REPORT_TEMPLATE_STYLESHEETS = [
    os.path.join(BASE_DIR, "apps/reporting/templates/report/html_default/report.css"),
]

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
