import json
from django import forms
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .models import Service
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
