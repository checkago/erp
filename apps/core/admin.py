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


class ErpUserAdmin(ImportExportModelAdmin, BaseUserAdmin):
    resource_class = ErpUserResource
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

    def save_model(self, request, obj, form, change):
        if not change:  # Если это создание нового пользователя
            obj.set_password(form.cleaned_data['password'])  # Устанавливаем зашифрованный пароль
        super().save_model(request, obj, form, change)


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
    list_display = ('id', 'full_name', 'short_name', 'manager')
    list_filter = ('manager',)

from django.contrib import admin
from .models import Branch

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'organization', 'full_name', 'short_name', 'manager',
                'address', 'mail_address', 'email', 'phone', 'department'
            )
        }),
        ('Тип библиотеки', {
            'fields': (
                'adult', 'child', 'child_young', 'village', 'mod_lib'
            )
        }),
        ('МАТЕРИАЛЬНО-ТЕХНИЧЕСКАЯ БАЗА', {
            'fields': (

            )
        }),
        ('Объекты культурного наследия', {
            'fields': (
                'object_federal_importance', 'object_regional_importance',
            )
        }),
        ('Доступность для лиц с ограниченными возможностями', {
            'fields': (
                'room_for_vision_disabled', 'room_for_hearing_disabled',
                'room_for_musculoskeletal_system_disabled'
            )
        }),
        ('Площадь помещений (м²)', {
            'fields': (
                'area_full', 'area_fund', 'area_work',
                'area_operation', 'area_rental', 'area_other'
            )
        }),
        ('Техническое состояние помещений', {
            'fields': (
                'area_repair', 'area_emergency', 'out_of_station_service_points'
            )
        }),
        ('Посадочные места', {
            'fields': (
                'seatings', 'seatings_computer', 'seatings_internet'
            )
        }),
        ('Автоматизированные технологии', {
            'fields': (
                'autotech_electronic_catalog', 'autotech_funds_disbursement',
                'autotech_user_access', 'autotech_funds_documents',
                'autotech_funds_digitization'
            )
        }),
        ('Прочее оборудование', {
            'fields': (
                'invalids_equipment', 'cars', 'cars_special'
            )
        }),
        ('Интернет и ресурсы', {
            'fields': (
                'availability_internet', 'availability_internet_for_users',
                'availability_site', 'availability_site_for_disabled'
            )
        }),
    )
    list_display = ('full_name', 'short_name', 'manager', 'adult', 'child', 'village')
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
admin.site.register(Cafedra, CafedraAdmin)
admin.site.register(Notification, NotificationAdmin)
