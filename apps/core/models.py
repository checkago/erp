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
    # Тип библиотеки
    adult = models.BooleanField(default=False, blank=True, verbose_name='Взрослая')
    child = models.BooleanField(default=False, blank=True, verbose_name='Детская')
    child_young = models.BooleanField(default=False, blank=True, verbose_name='Детско-Юношеская')
    village = models.BooleanField(default=False, blank=True, verbose_name='Сельская')
    mod_lib = models.BooleanField(default=False, blank=True, verbose_name='Модельная')

    # МАТЕРИАЛЬНО ТЕХНИЧЕСКАЯ БАЗА
    # Объекты культурного наследия
    object_federal_importance = models.BooleanField(default=False, verbose_name='Федерального значения')
    object_regional_importance = models.BooleanField(default=False, verbose_name='Регионального значения')

    # Здания (помещения), доступные для лиц
    room_for_vision_disabled = models.BooleanField(default=False, verbose_name='С нарушением зрения')
    room_for_hearing_disabled = models.BooleanField(default=False, verbose_name='С нарушением слуха')
    room_for_musculoskeletal_system_disabled = models.BooleanField(default=False,
                                                                   verbose_name='С нарушением опорно-двигательного аппарата')

    # Площадь помещений в м2
    area_full = models.DecimalField(default=0, max_digits=6, decimal_places=2, verbose_name='Общая площадь помещений в м2')
    area_fund = models.DecimalField(default=0, max_digits=6, decimal_places=2, verbose_name='Площадь для хранения фондов в м2')
    area_work = models.DecimalField(default=0, max_digits=6, decimal_places=2, verbose_name='Площадь для обслуживания пользователей в м2')

    # Площадь помещений по форме пользования м2
    area_operation = models.DecimalField(default=0,max_digits=6, decimal_places=2, verbose_name='В оперативном управлении')
    area_rental = models.DecimalField(default=0, max_digits=6, decimal_places=2, verbose_name='По договору аренды')
    area_other = models.DecimalField(default=0, max_digits=6, decimal_places=2,  verbose_name='Прочее')

    # Техническое состояние помещений (из гр. 10), м2
    area_repair = models.DecimalField(default=0, max_digits=6, decimal_places=2, verbose_name='Требует капитального ремонта')
    area_emergency = models.DecimalField(default=0, max_digits=6, decimal_places=2, verbose_name='Аварийное')
    out_of_station_service_points = models.IntegerField(default=0, verbose_name='Пункты вне стационарного обслуживания в ед.')

    # Число посадочных мест для пользователей, ед.
    seatings = models.IntegerField(default=0, verbose_name='Посадочные места')
    seatings_computer = models.IntegerField(default=0, verbose_name='Из них компьютеризованных')
    seatings_internet = models.IntegerField(default=0, verbose_name='с возможностью выхода в Интернет')

    # Наличие автоматизированных технологий (да - 1, нет - 0)
    autotech_electronic_catalog = models.BooleanField(default=True,
                                                      verbose_name='Обработка поступлений и ведения электронного каталога')
    autotech_funds_disbursement = models.BooleanField(default=True, verbose_name='Организация и учет выдачи фондов')
    autotech_user_access = models.BooleanField(default=True, verbose_name='Организация и учет доступа посетителей')
    autotech_funds_documents = models.BooleanField(default=True, verbose_name='Учет документов библиотечного фонда')
    autotech_funds_digitization = models.BooleanField(default=True, verbose_name='Для оцифровки фонда')

    # Средства для инвалидов
    invalids_equipment = models.BooleanField(default=True, verbose_name='Наличие оборудования для инвалидов')

    # Число транспортных средств, ед.
    cars = models.IntegerField(default=0, verbose_name='Всего транспортных средств')
    cars_special = models.IntegerField(default=0, verbose_name='Из них число специализированных транспортных средств')

    # Интернет и ресурсы
    availability_internet = models.BooleanField(default=True, verbose_name='Наличие интернета')
    availability_internet_for_users = models.BooleanField(default=True,
                                                          verbose_name='Наличие интернета для посетителей')
    availability_site = models.BooleanField(default=False, verbose_name='Наличие собственного Интернет-сайта')
    availability_site_for_disabled = models.BooleanField(default=False,
                                                         verbose_name='Наличие собственного Интернет-сайта для слабовидящих')

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


