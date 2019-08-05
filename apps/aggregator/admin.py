from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Service
from .utils import parse_docs


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('code', 'docs_url', 'last_update')
    readonly_fields = ('last_update', )
    exclude = ('json_data', )
    actions = ['update_docs']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        parse_docs(obj)

    def update_docs(self, request, queryset):
        for service in queryset:
            parse_docs(service)
    update_docs.short_description = _('Update documentation')
