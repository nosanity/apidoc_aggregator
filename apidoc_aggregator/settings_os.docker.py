import json
import os

if os.getenv('SECRET_KEY'):
    SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = str(os.getenv('DEBUG', True)) == 'True'

CONNECTION_TIMEOUT = int(os.getenv('CONNECTION_TIMEOUT', 10))
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL')
APIDOC_DB_NAME = os.getenv('APIDOC_DB_NAME', 'apidoc')
APIDOC_DB_USER = os.getenv('APIDOC_DB_USER', 'apidoc')
APIDOC_DB_PASSWORD = os.getenv('APIDOC_DB_PASSWORD', 'password')
APIDOC_DB_PORT = int(os.getenv('APIDOC_DB_PORT', 3306))
APIDOC_DB_HOST = os.getenv('APIDOC_DB_HOST', 'localhost')

if os.getenv('APIDOC_SWAGGER_SETTINGS'):
    SWAGGER_SETTINGS = json.loads(os.getenv('APIDOC_SWAGGER_SETTINGS'))
