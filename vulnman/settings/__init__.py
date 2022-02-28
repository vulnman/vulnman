"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""
import os
from split_settings.tools import optional, include
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

try:
    from vulnman.secret_key import SECRET_KEY
except ImportError:
    from vulnman.utils.secret import generate_secret_key
    generate_secret_key(os.path.join(BASE_DIR, 'vulnman/secret_key.py'))
    from vulnman.secret_key import SECRET_KEY

base_settings = [
    "base.py",
    "apps.py",
    "database.py",
    "orig.py",
    "plugins.py",
    "reporting.py",
    "rest_framework.py",
    optional(os.path.join(BASE_DIR, "local_settings.py"))
]

include(*base_settings)
