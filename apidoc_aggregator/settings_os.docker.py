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

SSO_UNTI_URL = os.getenv('SSO_UNTI_URL', '')
SOCIAL_AUTH_UNTI_KEY = os.getenv('SOCIAL_AUTH_UNTI_KEY', '')
SOCIAL_AUTH_UNTI_SECRET = os.getenv('SOCIAL_AUTH_UNTI_SECRET', '')
SSO_API_KEY = os.getenv('SSO_API_KEY', '')

API_KEY = os.getenv('API_KEY', '')

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'openapi')
KAFKA_HOST = os.getenv('KAFKA_HOST', '')
KAFKA_PORT = os.getenv('KAFKA_PORT', '')
KAFKA_PROTOCOL = os.getenv('KAFKA_PROTOCOL', 'https')
KAFKA_TOKEN = os.getenv('KAFKA_TOKEN', '')

KONG_API_URL = os.getenv('KONG_API_URL', '')
PUBLIC_KONG_CONSUMER = os.getenv('PUBLIC_KONG_CONSUMER', 'unti_users')
PUBLIC_KONG_GROUP = os.getenv('PUBLIC_KONG_GROUP', 'public')

SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', '')

if os.getenv('APIDOC_SWAGGER_SETTINGS'):
    SWAGGER_SETTINGS = json.loads(os.getenv('APIDOC_SWAGGER_SETTINGS'))
