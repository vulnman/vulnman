# This is an example settings file for vulnman


# Enable debug mode. DONT USE IN PRODUCTION ENVIRONMENT!
# DEBUG = True

# Allowed Hosts
# set this to the hostnames of allowed to be used in the Host HTTP header
# ALLOWED_HOSTS = ["vulnman.example.com"]


# CSS theme
# VULNMAN_CSS_THEME = "flatly"

# #################
# Database Settings
# #################
# uncomment the postgres section, if you are using the docker image
#
# Postgres Example:
#
# DATABASES = {
#  'default': {
#    'ENGINE': 'django.db.backends.postgresql',
#    'HOST': 'db',
#    'NAME': 'vulnman',
#    'USER': 'vulnman_db_user',
#    'PASSWORD': 'dontusethispassword',
#  }
# }

# ##############
# External Tools
# ##############
# add your own custom tools classes here
# CUSTOM_EXTERNAL_TOOLS = {
#     "my-new-nmap-parser": "apps.external_tools.parsers.nmap.NmapParser",
# }

# #########
# Reporting
# #########

# Pentest company name
# This name is used in some parts of the reports. This usually is the name of your company.
# REPORT_PENTEST_COMPANY = "Example IT-Sec Ltd."

# Path to the latex interpreter used to generate the reports
# LATEX_INTERPRETER = 'latexmk -pdf'

# Report Template
# REPORT_TEMPLATE = "custom/report/document.tex"
