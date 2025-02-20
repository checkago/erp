from django.contrib import admin

from apps.reports.models import Event, VisitReport, BookReport, VisitPlan, EventsPlan, BookPlan, RegsPlan, \
    RegsFirstData, VisitsFirstData, EventsFirstData, BooksFirstData


class EventAdmin(admin.ModelAdmin):
    list_display = ('date', 'library', 'cafedra', 'name', 'direction', 'paid', 'note')
    list_filter = ('date', 'library', 'cafedra', 'paid')


class VisitReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'library', 'cafedra', 'note')
    list_filter = ('date', 'library', 'cafedra')


class BookReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'library', 'cafedra', 'note')
    list_filter = ('date', 'library', 'cafedra')


class EventsPlanAdmin(admin.ModelAdmin):
    list_display = ('year', 'library', 'total_events')
    list_filter = ('year', 'library')


class BooksPlanAdmin(admin.ModelAdmin):
    list_display = ('year', 'library', 'total_books')
    list_filter = ('year', 'library')


class VisitsPlanAdmin(admin.ModelAdmin):
    list_display = ('year', 'library', 'total_visits')
    list_filter = ('year', 'library')


class RegsPlanAdmin(admin.ModelAdmin):
    list_display = ('year', 'library', 'total_regs')
    list_filter = ('year', 'library')


class RegsFirstDataAdmin(admin.ModelAdmin):
    list_display = ('library', 'data')


class VisitsFirstDataAdmin(admin.ModelAdmin):
    list_display = ('library', 'data')


class EventsFirstDataAdmin(admin.ModelAdmin):
    list_display = ('library', 'data')


class BooksFirstDataAdmin(admin.ModelAdmin):
    list_display = ('library', 'data')


admin.site.register(Event, EventAdmin)
admin.site.register(VisitReport, VisitReportAdmin)
admin.site.register(BookReport, BookReportAdmin)
admin.site.register(VisitPlan, VisitsPlanAdmin)
admin.site.register(EventsPlan, EventsPlanAdmin)
admin.site.register(BookPlan, BooksPlanAdmin)
admin.site.register(RegsPlan, RegsPlanAdmin)
admin.site.register(RegsFirstData, RegsFirstDataAdmin)
admin.site.register(VisitsFirstData, VisitsFirstDataAdmin)
admin.site.register(EventsFirstData, EventsFirstDataAdmin)
admin.site.register(BooksFirstData, BooksFirstDataAdmin)



