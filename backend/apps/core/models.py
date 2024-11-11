from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    email = models.EmailField(verbose_name='E-mail')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    middle_name = models.CharField(max_length=150, blank=True, verbose_name='Отчество')
    avatar = models.ImageField(upload_to='users_avatars/', default='default_avatar.png', verbose_name='Аватар')
    enabled = models.BooleanField(default=True, verbose_name='Включен')

    notify_tasks = models.BooleanField(default=True, verbose_name="Оповещать о задачах")
    notify_messages = models.BooleanField(default=True, verbose_name="Оповещать о сообщениях")
    notify_documents = models.BooleanField(default=True, verbose_name="Оповещать о документах")
    active = models.BooleanField(default=True, verbose_name="Включен")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.username})'

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"