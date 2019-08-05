from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField


class Service(models.Model):
    code = models.SlugField(unique=True, verbose_name=_('Unique code for system'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    docs_url = models.URLField(verbose_name=_('Url for documentation description'))
    prefixes = JSONField(default=dict, blank=True, help_text=_(
        'Example: {"": "uploads-public", "api_key": "uploads"}. '
        'If security parameters contain "api_key", the prefix /uploads will be used, otherwise /uploads-public'
    ))
    security_overrides = JSONField(default=dict, blank=True, help_text=_(
        'Substitution for security definition. For example, '
        '{"api_key": {"type": "apiKey", "name": "x-kong-api", "in": "header"}}'
    ))
    json_data = JSONField(default=dict)
    last_update = models.DateTimeField(null=True, default=None, blank=True)
