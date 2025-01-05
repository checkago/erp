from datetime import datetime

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class ErpUser(AbstractUser, PermissionsMixin):
    last_name = models.CharField(max_length=150, default='Фамилия', verbose_name='Фамилия')
    first_name = models.CharField(max_length=150, default='Имя', verbose_name='Имя')
    middle_name = models.CharField(max_length=150, blank=True, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Email', unique=True)
    avatar = models.ImageField(upload_to='users/avatar', verbose_name='Аватар',
                               default='users/blank_avatar.jpg', blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация')
    is_active = models.BooleanField(default=True, verbose_name='Включен')
    is_staff = models.BooleanField(default=True, verbose_name='Статус персонала')
    task_notifications = models.BooleanField(default=False, verbose_name='Уведомления о задачах')
    messages_notifications = models.BooleanField(default=False, verbose_name='Уведомления о сообщениях')
    events_notifications = models.BooleanField(default=False, verbose_name='Уведомления о событиях')

    groups = models.ManyToManyField('auth.Group', verbose_name="groups", blank=True,
                                    related_name="erp_user_groups", related_query_name="erp_user")
    user_permissions = models.ManyToManyField('auth.Permission', verbose_name="user permissions", blank=True,
                                              related_name="erp_user_permissions", related_query_name="erp_user")

    class Meta:
        verbose_name = 'Пользователь портала'
        verbose_name_plural = 'Пользователи портала'

    def __str__(self):
        return self.username


class Position(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование должности', unique=False)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                               db_index=True, verbose_name='Руководитель')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Список должностей'

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(ErpUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    position = models.ForeignKey(Position, verbose_name='Должность', on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey('Branch', verbose_name='Филиал', on_delete=models.CASCADE, blank=True, null=True,
                               related_name='employees')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True, null=True)
    start_date = models.DateField(verbose_name='Дата приема', blank=True, null=True)
    dismissed = models.BooleanField(default=False, verbose_name='Уволен')
    end_date = models.DateField(verbose_name='Дата увольнения', blank=True, null=True)
    vacancy = models.BooleanField(default=False, verbose_name='Отпуск')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники организации'

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class Organization(models.Model):
    full_name = models.CharField(max_length=250, verbose_name='Полное наименование')
    short_name = models.CharField(max_length=150, verbose_name='Краткое наименование')
    manager = models.ForeignKey(Employee, verbose_name='Директор', related_name='organization_manager_set',
                                on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=250, blank=True, verbose_name='Адрес юридический')
    mail_address = models.CharField(max_length=250, blank=True, verbose_name='Адрес почтовый')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    site = models.URLField(blank=True, verbose_name='Сайт')
    inn = models.CharField(max_length=10, blank=True, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, blank=True, verbose_name='КПП')
    ogrn = models.CharField(max_length=13, blank=True, verbose_name='ОГРН')
    reg_date = models.DateField(verbose_name='дата регистрации', blank=True, null=True)
    logo_big = models.ImageField(upload_to='organization/logo', verbose_name='Большой логотип', blank=True, null=True)
    logo_small = models.ImageField(upload_to='organization/logo', verbose_name='Маленький логотип', blank=True, null=True)
    logo_vertical = models.ImageField(upload_to='organization/logo', verbose_name='Вертикальный логотип', blank=True,
                                   null=True)

    class Meta:
        verbose_name = 'Данные организации'
        verbose_name_plural = 'Список организаций'

    def __str__(self):
        return self.short_name


class Branch(models.Model):
    organization = models.ForeignKey(Organization, verbose_name='Организация', on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=250, verbose_name='Полное наименование')
    short_name = models.CharField(max_length=150, verbose_name='Краткое наименование')
    manager = models.ForeignKey(Employee, verbose_name='Заведующий', related_name='branch_manager_set',
                                on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=250, blank=True, verbose_name='Адрес юридический')
    mail_address = models.CharField(max_length=250, blank=True, verbose_name='Адрес почтовый')
    email = models.EmailField(max_length=250, blank=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    department = models.BooleanField(default=False, blank=True, verbose_name='Это отдел')
    adult = models.BooleanField(default=False, blank=True, verbose_name='Взрослая библиотека')
    child = models.BooleanField(default=False, blank=True, verbose_name='Детская')
    mod_lib = models.BooleanField(default=False, blank=True, verbose_name='Модельная')

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return self.short_name

    def get_employees(self):
        return Employee.objects.filter(branch=self).order_by('user__last_name', 'user__first_name')

    def get_cafedra_set(self):
        return Cafedra.objects.filter(branch=self).order_by('name')


class Cafedra(models.Model):
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Библиотека/Филиал',
                                related_name='cafedra_set', null=True)
    name = models.CharField(max_length=150, verbose_name='Название кафедры')

    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'

    def __str__(self):
        return self.name


class Notification(models.Model):
    FIRE = 'Срочно'
    SIMPLE = 'Внимание'
    VIEW = 'Рассмотреть'

    Notification_CHOICES = (
        (FIRE, 'Срочно'),
        (SIMPLE, 'Внимание'),
        (VIEW, 'Рассмотреть')
    )

    importance = models.CharField(max_length=150, choices=Notification_CHOICES, default=SIMPLE,
                                  verbose_name='Важность')
    date = models.DateField(default=datetime.now, verbose_name='Дата')
    days = models.IntegerField(verbose_name='Количество дней публикации', null=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Текст')
    link = models.URLField(blank=True, verbose_name='Ссылка')
    active = models.BooleanField(default=True, verbose_name='Включено')

    class Meta:
        verbose_name = 'Сообщение аппбара'
        verbose_name_plural = 'Сообщения для шапки'

    def __str__(self):
        return self.title


