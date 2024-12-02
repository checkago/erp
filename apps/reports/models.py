import datetime

from django.db import models

from apps.core.models import Branch


#Массовые мероприятия
class Event(models.Model):
    
    DN = 'Досуговое направление'
    DNN = 'Духовно-нравственное, эстетическое направление'
    IPN = 'Историко-патриотическое направление'
    KR = 'Краеведение'
    NPN = 'Научно-популярное направление'
    PPNTAT = 'Профилактика правонарушений, в т.ч. наркомании, токсикомании, алкоголизма, табакокурения'
    PSPN = 'Профилактика суицидального поведения несовершеннолетних'
    PTE = 'Профилактика терроризма и экстремизма'
    PO = 'Профориентация'
    SKAM = 'Социальная и культурная адаптация мигрантов'
    UMMS = 'Укрепление межнационального и межрелигиозного согласия'
    UOZ = 'Укрепление общественного здоровья'
    EP = 'Экологическое просвещение'

    direction_CHOICES = (
        (DN, 'Досуговое направление'),
        (DNN, 'Духовно-нравственное, эстетическое направление'),
        (IPN, 'Историко-патриотическое направление'),
        (KR, 'Краеведение'),
        (NPN, 'Научно-популярное направление'),
        (PPNTAT, 'Профилактика правонарушений, в т.ч. наркомании, токсикомании, алкоголизма, табакокурения'),
        (PSPN, 'Профилактика суицидального поведения несовершеннолетних'),
        (PTE, 'Профилактика терроризма и экстремизма'),
        (PO, 'Профориентация'),
        (SKAM, 'Социальная и культурная адаптация мигрантов'),
        (UMMS, 'Укрепление межнационального и межрелигиозного согласия'),
        (UOZ, 'Укрепление общественного здоровья'),
        (EP, 'Экологическое просвещение')
    )

    CHILD = 'Дети'
    ADULT = 'Взрослые'
    OTHER = 'Пожилые/Прочие'

    age_CHOICES = (
        (CHILD, 'Дети'),
        (ADULT, 'Взрослые'),
        (OTHER, 'Пожилые/Прочие'),
    )
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Библиотека')
    name = models.CharField(max_length=250, verbose_name='Название мероприятия')
    date = models.DateTimeField(verbose_name='Дата проведения')
    direction = models.CharField(max_length=150, choices=direction_CHOICES, default=IPN,
                                  verbose_name='Направление')
    quantity = models.IntegerField(default=0, verbose_name='Количество мероприятий')
    age_group = models.CharField(max_length=150, choices=age_CHOICES, default=ADULT,
                                 verbose_name='Возрастная группа')
    age_14 = models.IntegerField(default=0, verbose_name='До 14')
    age_35 = models.IntegerField(default=0, verbose_name='До 35')
    age_54 = models.IntegerField(default=0, verbose_name='До 55')
    age_other = models.IntegerField(default=0, verbose_name='После 55 и другие')
    invalids = models.IntegerField(default=0, verbose_name='Инвалиды')
    out_of_station = models.IntegerField(default=0, verbose_name='Внестационар')
    note = models.TextField(verbose_name='Примечание', blank=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Массовые мероприятия'

    def __str__(self):
        return f"{self.date} {self.name} {self.direction}"


#Показатели детской библиотеки
class ChildLibrary(models.Model):
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Библиотека')

    class Meta:
        verbose_name = 'Детская библиотека'
        verbose_name_plural = 'Детские библиотеки'

    def __str__(self):
        return f"{self.library} {len(self.cafedra)}"


