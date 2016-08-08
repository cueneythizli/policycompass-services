__author__ = 'fki'

from .settings_basic import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'pcompass.db',
    }
}

# Database config example for PostgreSQL

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'pcompass',
#         'USER': 'pcompass',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#     }
# }

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ELASTICSEARCH_URL = 'http://localhost:9200/policycompass_search/'

PC_SERVICES = {
    'references': {
        'frontend_base_url': 'http://localhost:9000',
        'MEDIA_URL' : 'media/',
        'base_url': 'http://localhost:8000',
        'units': '/api/v1/references/units',
        'external_resources': '/api/v1/references/externalresources',
        'languages': '/api/v1/references/languages',
        'domains': '/api/v1/references/policydomains',
        'dateformats': '/api/v1/references/dateformats',
        'licenses': '/api/v1/references/licenses',
        'eventsInVisualizations': '/api/v1/visualizationsmanager/eventsInVisualizations',
        #'metricsInvisualizations': '/api/v1/visualizationsmanager/metricsInVisualizations',
        'datasetsInvisualizations': '/api/v1/visualizationsmanager/datasetsInVisualizations',
        'updateindexitem' : '/api/v1/searchmanager/updateindexitem',
        'deleteindexitem' : '/api/v1/searchmanager/deleteindexitem',
        'fcm_base_url': 'http://localhost:8080',
        'adhocracy_api_base_url': 'http://localhost:6541'
    },
}
