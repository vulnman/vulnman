import os
from vulnman.settings import BASE_DIR


VULNMAN_CSS_THEME = "vulnman-dark"

HOST_OS_ICONS = {
    "linux": {
        "icon": "fa fa-linux", "matches": ["Ubuntu", "Fedora", "Arch-Linux", "Debian", "Linux"]
    }
}

CUSTOM_EXTERNAL_TOOLS = {}

REPORT_SECTION_DEFAULTS_DIR = os.path.join(BASE_DIR, "apps/reporting/templates/report/html_default/defaults")

REPORT_SECTIONS = {
    "assessment_overview": os.path.join(REPORT_SECTION_DEFAULTS_DIR, "02_assessment_overview.md"),
    "methodology": os.path.join(REPORT_SECTION_DEFAULTS_DIR, "03_methodology.md")
}
CUSTOM_REPORT_SECTIONS = {}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

