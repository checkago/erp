from django.contrib import admin

from apps.reports.models import Event, VisitReport, BookReport


class EventAdmin(admin.ModelAdmin):
    list_display = ('date', 'library', 'cafedra', 'name', 'direction', 'paid', 'note')
    list_filter = ('date', 'library', 'cafedra', 'paid')


class VisitReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'library', 'cafedra', 'note')
    list_filter = ('date', 'library', 'cafedra')


class BookReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'library', 'cafedra', 'note')
    list_filter = ('date', 'library', 'cafedra')


admin.site.register(Event, EventAdmin)
admin.site.register(VisitReport, VisitReportAdmin)
admin.site.register(BookReport, BookReportAdmin)
