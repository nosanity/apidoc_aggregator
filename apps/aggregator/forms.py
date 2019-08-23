from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.aggregator.api import SSOApi, ApiError
from apps.aggregator.models import ClientRegistrationRequest


class ClientRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = ClientRegistrationRequest
        fields = ['redirect_uri']

    def clean_redirect_uri(self):
        redirect_uri = self.cleaned_data.get('redirect_uri')
        if redirect_uri:
            try:
                resp = SSOApi().check_oauth_client(redirect_uri)
                if resp['exists']:
                    raise forms.ValidationError(_('Client with redirect uri %s exists') % redirect_uri)
            except (ApiError, KeyError):
                raise forms.ValidationError(_('Failed to check if client with requested redirect uri exists'))
        return redirect_uri

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.user = self.request.user
        if commit:
            obj.save()
        return obj
