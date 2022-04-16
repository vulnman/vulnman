import os
from vulnman.settings import BASE_DIR


VULNMAN_CSS_THEME = "vulnman-dark"

HOST_OS_ICONS = {
    "linux": {
        "icon": "fa fa-linux", "matches": ["Ubuntu", "Fedora", "Arch-Linux", "Debian", "Linux"]
    }
}

CUSTOM_EXTERNAL_TOOLS = {}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

VULNERABILITY_TEMPLATE_REPO = "https://github.com/vulnman/community-vulnerability-templates"
CHECKLIST_REPO = "https://github.com/vulnman/community-checklists"
