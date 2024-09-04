# backend/apps/users/models.py

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя, расширяющая стандартную модель Django.
    """
    # Дополнительные поля можно добавить здесь
    pass
