import os
import sys
import site

SETTINGS_DIR = os.path.realpath(
        os.path.join(os.path.dirname(__file__), os.path.sep.join(('..',) * 2)))

sys.path.append(SETTINGS_DIR)
site.addsitedir(SETTINGS_DIR + '/vendor')
from funfactory import manage
manage.ROOT = SETTINGS_DIR
import settings

s = settings.DATABASES['default']
MYSQL_PASS = s['PASSWORD']
MYSQL_USER = s['USER']
MYSQL_HOST = s.get('HOST', 'localhost')
MYSQL_NAME = s['NAME']

CATALOG_PATH      = settings.SPHINX_CATALOG_PATH
LOG_PATH          = settings.SPHINX_LOG_PATH
ETC_PATH          = os.path.dirname(settings.SPHINX_CONFIG_PATH)
LISTEN_PORT       = settings.SPHINX_PORT
MYSQL_LISTEN_PORT = settings.SPHINXQL_PORT
MYSQL_LISTEN_HOST = 'localhost'

if MYSQL_HOST.endswith('.sock'):
    MYSQL_HOST = 'localhost'

if os.environ.get('DJANGO_ENVIRONMENT') == 'test':
    MYSQL_NAME = 'test_' + MYSQL_NAME
    LISTEN_PORT       = settings.TEST_SPHINX_PORT
    MYSQL_LISTEN_PORT = settings.TEST_SPHINXQL_PORT
    CATALOG_PATH      = settings.TEST_SPHINX_CATALOG_PATH
    LOG_PATH          = settings.TEST_SPHINX_LOG_PATH
