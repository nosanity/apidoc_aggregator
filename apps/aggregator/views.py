import json
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework_swagger.settings import swagger_settings
from .models import Service
from .utils import transform_documentation


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({
            'services': Service.objects.order_by('title'),
        })
        return data


class SystemDocumentation(TemplateView):
    template_name = 'service_docs.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        system = get_object_or_404(Service, code=self.kwargs['code'])
        data.update({
            'service': system,
            'spec': json.dumps(transform_documentation(system, self.request)),
            'drs_settings': json.dumps(self.get_ui_settings())
        })
        return data

    def get_ui_settings(self):
        data = {
            'apisSorter': swagger_settings.APIS_SORTER,
            'docExpansion': swagger_settings.DOC_EXPANSION,
            'jsonEditor': swagger_settings.JSON_EDITOR,
            'operationsSorter': swagger_settings.OPERATIONS_SORTER,
            'showRequestHeaders': swagger_settings.SHOW_REQUEST_HEADERS,
            'supportedSubmitMethods': swagger_settings.SUPPORTED_SUBMIT_METHODS,
            'acceptHeaderVersion': swagger_settings.ACCEPT_HEADER_VERSION,
            'customHeaders': swagger_settings.CUSTOM_HEADERS,
        }
        if swagger_settings.VALIDATOR_URL != '':
            data['validatorUrl'] = swagger_settings.VALIDATOR_URL
        return data
