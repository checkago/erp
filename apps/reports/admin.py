from django.contrib import admin

from apps.reports.models import Event, AdultVisitReport, AdultBookReport, ChildBookReport, ChildVisitReport


class EventAdmin(admin.ModelAdmin):
    list_display = ('date', 'library', 'cafedra', 'name', 'direction', 'paid')
    list_filter = ('date', 'library', 'cafedra', 'paid')


class AdultVisitReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'library')


class AdultBookReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'library')


class ChildVisitReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'library')


class ChildBookReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'library')


admin.site.register(Event, EventAdmin)
admin.site.register(AdultVisitReport, AdultVisitReportAdmin)
admin.site.register(AdultBookReport, AdultBookReportAdmin)
admin.site.register(ChildVisitReport, ChildVisitReportAdmin)
admin.site.register(ChildBookReport, ChildBookReportAdmin)
