# models.py

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class User(AbstractUser):
    # Additional fields
    middle_name = models.CharField(max_length=150, blank=True, verbose_name=_("Отчество"))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_("Дата рождения"))
    date_of_hire = models.DateField(verbose_name=_("Дата приема на работу"))
    position = models.CharField(max_length=255, blank=True, verbose_name=_("Должность"))
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True, default='user_photos/default_avatar.png',
                              verbose_name=_("Фото"))
    work_phone = models.CharField(max_length=50, verbose_name=_("Рабочий телефон"))
    mobile_phone = models.CharField(max_length=50, verbose_name=_("Мобильный телефон"))
    comment = models.TextField(blank=True, verbose_name=_("Комментарий"))

    NOTIFY_CHOICES = [
        (True, _("Оповещать")),
        (False, _("Не оповещать")),
    ]
    notification_settings = models.BooleanField(choices=NOTIFY_CHOICES, default=True,
                                                verbose_name=_("Настройки оповещения"))

    # Adjusted related_name to avoid clashes
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='custom_user_group',
                              verbose_name=_("Группа"))
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', verbose_name=_("Группы"), blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions',
                                              verbose_name=_("Разрешения"), blank=True)

    def __str__(self):
        return f'{self.username} ({self.first_name} {self.last_name})'

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
