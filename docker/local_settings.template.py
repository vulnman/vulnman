import os
# This is an example settings file for vulnman docker


# Enable debug mode. DONT USE IN PRODUCTION ENVIRONMENT!
# DEBUG = True

# Allowed Hosts
# set this to the hostnames of allowed to be used in the Host HTTP header
ALLOWED_HOSTS = ["vulnman-web"]

# Required Setting:
CSRF_TRUSTED_ORIGINS = os.environ.get("VULNMAN_CSRF_TRUSTED_ORIGINS", "https://localhost").split(",")

# #################
# Database Settings
# #################
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'HOST': 'db',
    'NAME': os.environ.get('VULNMAN_DB_NAME', 'vulnman'),
    'USER': os.environ.get('VULNMAN_DB_USER', 'vulnman_db_user'),
    'PASSWORD': os.environ.get("VULNMAN_DB_PASSWORD", "dontusethispassword"),
  }
}
