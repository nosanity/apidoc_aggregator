import json
import logging
from django import forms
from django.contrib import admin, messages
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from apps.aggregator.api import SSOApi, ApiError
from .models import Service, ClientRegistrationRequest
from .utils import parse_docs


class ServiceForm(forms.ModelForm):
    json_file = forms.FileField(
        required=False,
        help_text=_('Use editor at <a href="{url}" target="_blank">{url}</a> to generate documentation').format(
            url='https://editor.swagger.io/')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['docs_url'].required = False

    def clean(self):
        data = super().clean()
        msg = _('"{field}" or "Json file" should be defined, but not both').format(
                field=Service._meta.get_field('docs_url').verbose_name)
        if not self.cleaned_data.get('docs_url'):
            if not self.cleaned_data.get('json_file'):
                if self.instance and self.instance.json_data:
                    self.cleaned_data['json_file'] = self.instance.json_data
                else:
                    raise forms.ValidationError(msg)
        elif bool(self.cleaned_data.get('docs_url')) == bool(self.cleaned_data.get('json_file')):
            raise forms.ValidationError(msg)
        return data

    def clean_json_file(self):
        data = self.cleaned_data.get('json_file')
        if data:
            try:
                data.seek(0)
                data = json.loads(data.read().decode('utf8'))
            except:
                raise forms.ValidationError(_('Invalid data'))
        return data

    def save(self, commit=False):
        obj = super().save(commit=False)
        if not self.cleaned_data.get('docs_url'):
            obj.json_data = self.cleaned_data.get('json_file')
            obj.last_update = timezone.now()
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Service
        fields = '__all__'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('code', 'docs_url', 'last_update')
    readonly_fields = ('last_update', )
    exclude = ('json_data', )
    actions = ['update_docs']
    form = ServiceForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        parse_docs(obj)

    def update_docs(self, request, queryset):
        for service in queryset:
            parse_docs(service)
    update_docs.short_description = _('Update documentation')


@admin.register(ClientRegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'redirect_uri', 'status', 'created_at', 'updated_at')
    readonly_fields = ('user', 'redirect_uri')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj=obj)
        if obj and obj.status == ClientRegistrationRequest.STATUS_ACCEPTED:
            fields += ('status', )
        return fields

    def save_model(self, request, obj, form, change):
        old_status = ClientRegistrationRequest.objects.get(id=obj.id).status
        if obj.status == ClientRegistrationRequest.STATUS_ACCEPTED:
            try:
                SSOApi().create_oauth_client(obj.redirect_uri, obj.user.email)
            except ApiError:
                logging.exception('Failed to create oauth client')
                obj.status = old_status
                self.message_user(request, _('Failed to create oauth client: communication with sso failed'),
                                  messages.ERROR)
        super().save_model(request, obj, form, change)
