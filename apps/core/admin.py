from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from datetime import datetime, date

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import ErpUser, Position, Employee, Organization, Branch, Notification, Cafedra


class ErpUserResource(resources.ModelResource):
    class Meta:
        model = ErpUser
        # Укажите дополнительные настройки, если необходимо


class ErpUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ErpUserResource  # Укажите ресурс для экспорта/импорта
    list_display = ('username', 'email', 'last_name', 'first_name', 'middle_name',
                    'is_staff', 'is_active', 'task_notifications',
                    'messages_notifications', 'events_notifications')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'middle_name',
                                      'email', 'avatar')}),
        ('Additional Fields', {'fields': ('birth_date', 'bio',
                                          'task_notifications',
                                          'messages_notifications',
                                          'events_notifications')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Additional Fields', {'fields': ('email', 'birth_date',
                                          'bio',
                                          'task_notifications',
                                          'messages_notifications',
                                          'events_notifications')}),
    )


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'position', 'branch')
    list_filter = ('position', 'branch')

    @admin.display(description='ФИО')
    def get_full_name(self, obj):
        return f"{obj.user.last_name} {obj.user.first_name} {obj.user.middle_name}"


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'short_name', 'manager')
    list_filter = ('manager',)


class BranchAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'short_name', 'manager', 'adult', 'child')
    list_filter = ('organization', 'manager', 'adult', 'child')


class CafedraAdmin(admin.ModelAdmin):
    list_display = ('name', 'library')
    list_filter = ('library',)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'importance', 'date', 'days', 'active')
    list_filter = ('importance', 'date', 'active')

    class WarningsAdmin(admin.ModelAdmin):
        list_display = ('title', 'importance', 'date', 'days', 'active')
        list_filter = ('importance', 'date', 'active')

        def get_form(self, request, obj=None, **kwargs):
            form = super().get_form(request, obj, **kwargs)
            if obj:
                expiration_date = timezone.make_aware(datetime.combine(obj.date, datetime.min.time()))
                if obj.days:
                    expiration_date += timezone.timedelta(days=obj.days)
                if expiration_date < timezone.now():
                    form.base_fields['active'].disabled = True
            return form


admin.site.register(ErpUser, ErpUserAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Cafedra, CafedraAdmin)
admin.site.register(Notification, NotificationAdmin)
