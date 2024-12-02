from django.contrib import admin

from apps.reports.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'direction')


admin.site.register(Event, EventAdmin)
