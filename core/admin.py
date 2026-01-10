from django.contrib import admin
from .models import EHRConnection, WebHook

class WebHookAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['is_active', 'is_verified']

        elif obj is not None:
            if obj.is_verified:
                return ['is_verified']

            return ['is_active', 'is_verified']


admin.site.register(EHRConnection)
admin.site.register(WebHook, WebHookAdmin)
