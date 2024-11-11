from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('avatar_thumbnail', 'user', 'email', 'last_name', 'first_name', 'id')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    ordering = ('user',)

    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" style="width: 50px; height: auto;"/>')
        return "Нет изображения"

    avatar_thumbnail.short_description = 'Миниатюра'

