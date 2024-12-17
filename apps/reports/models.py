import datetime

from django.db import models

from apps.core.models import Branch, Cafedra


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

    KRUJKI = 'Кружки'
    AD = 'Активное долголетие'
    OTHER = 'Прочие'

    age_CHOICES = (
        (KRUJKI, 'Кружки'),
        (AD, 'Активное долголетие'),
        (OTHER, 'Прочие'),
    )
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Библиотека')
    cafedra = models.ForeignKey(Cafedra, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Кафедра')
    name = models.CharField(max_length=250, verbose_name='Название мероприятия')
    date = models.DateField(verbose_name='Дата проведения')
    direction = models.CharField(max_length=150, choices=direction_CHOICES, default=IPN,
                                  verbose_name='Направление')
    quantity = models.IntegerField(default=1, verbose_name='Количество мероприятий')
    age_14 = models.IntegerField(default=0, verbose_name='До 14')
    age_35 = models.IntegerField(default=0, verbose_name='До 35')
    age_other = models.IntegerField(default=0, verbose_name='После 35 и другие')
    invalids = models.IntegerField(default=0, verbose_name='Инвалиды')
    out_of_station = models.IntegerField(default=0, verbose_name='Внестационар')
    as_part = models.CharField(max_length=150, choices=age_CHOICES, default=KRUJKI,
                                 verbose_name='В рамках')
    paid = models.BooleanField(default=False, blank=True, verbose_name='Платное')
    note = models.TextField(verbose_name='Примечание', blank=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Массовые мероприятия'

    def __str__(self):
        return f"{self.date} {self.name} {self.direction}"


#Показатели детской библиотеки
class ChildVisitReport(models.Model):
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Библиотека')
    cafedra = models.ForeignKey(Cafedra, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Кафедра')
    date = models.DateField(null=True, verbose_name='Дата отчета')
    qty_reg_7 = models.IntegerField(default=0, verbose_name='Новые (Дошкольники)')
    qty_reg_14 = models.IntegerField(default=0, verbose_name='Новые (Остальные - 14)')
    qty_reg_30 = models.IntegerField(default=0, verbose_name='Новые (Молодежь 15-30)')
    qty_reg_other = models.IntegerField(default=0, verbose_name='Новые (Прочие 30+)')
    qty_visited_14 = models.IntegerField(default=0, verbose_name='Посещение (Остальные - 14)')
    qty_visited_35 = models.IntegerField(default=0, verbose_name='Посещение (Молодежь 15-30)')
    qty_visited_other = models.IntegerField(default=0, verbose_name='Посещение (Прочие 30+)')
    qty_visited_invalids = models.IntegerField(default=0, verbose_name='Посещение (Инвалиды)')
    qty_visited_out_station = models.IntegerField(default=0, verbose_name='Посещение (Внестационар)')
    qty_events_14 = models.IntegerField(default=0, verbose_name='Мероприятия (Остальные - 14)')
    qty_events_35 = models.IntegerField(default=0, verbose_name='Мероприятия (Молодежь 15-30)')
    qty_events_other = models.IntegerField(default=0, verbose_name='Мероприятия (Прочие 30+)')
    qty_events_invalids = models.IntegerField(default=0, verbose_name='Мероприятия (Инвалиды)')
    qty_events_out_station = models.IntegerField(default=0, verbose_name='Мероприятия (Внестационар)')
    qty_online_requests = models.IntegerField(default=0, verbose_name='Удаленные обращения')
    qty_paid = models.IntegerField(default=0, verbose_name='Платные посещения')
    note = models.TextField(blank=True, verbose_name='Примечание')

    class Meta:
        verbose_name = 'Отчет посещений по детской библиотеке'
        verbose_name_plural = 'Отчеты посещений по детским библиотекам'

    def __str__(self):
        return f"{self.library}"


class ChildBookReport(models.Model):
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Библиотека')
    cafedra = models.ForeignKey(Cafedra, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Кафедра')
    date = models.DateField(null=True, verbose_name='Дата отчета')
    qty_books_14 = models.IntegerField(default=0, verbose_name='Книговыдача (До 14)')
    qty_books_30 = models.IntegerField(default=0, verbose_name='Книговыдача (15-30)')
    qty_books_other = models.IntegerField(default=0, verbose_name='Книговыдача (Прочие)')
    qty_books_part_opl = models.IntegerField(default=0, verbose_name='Общ.-политтич.лит-ра')
    qty_books_part_enm = models.IntegerField(default=0, verbose_name='Естеств. Науки. Медицина')
    qty_books_part_tech = models.IntegerField(default=0, verbose_name='Техника')
    qty_books_part_sh = models.IntegerField(default=0, verbose_name='Сельское хозяйство')
    qty_books_part_si= models.IntegerField(default=0, verbose_name='Спорт. Искусство')
    qty_books_part_yl = models.IntegerField(default=0, verbose_name='Языкознание. Литературоведение')
    qty_books_part_hl = models.IntegerField(default=0, verbose_name='Художественная лит-ра')
    qty_books_part_dl = models.IntegerField(default=0, verbose_name='Детская литература')
    qty_books_part_other = models.IntegerField(default=0, verbose_name='Прочие(в т.ч. журналы)')
    qty_books_part_audio = models.IntegerField(default=0, verbose_name='Аудиокниги')
    qty_books_part_krai = models.IntegerField(default=0, verbose_name='Краеведение(в том числе)')
    qty_books_reference_14 = models.IntegerField(default=0, verbose_name='Справки (14)')
    qty_books_reference_30 = models.IntegerField(default=0, verbose_name='Справки (30)')
    qty_books_reference_other = models.IntegerField(default=0, verbose_name='Справки (Прочие)')
    qty_books_reference_online = models.IntegerField(default=0, verbose_name='Справки (Удаленно')
    note = models.TextField(blank=True, verbose_name='Примечание')


    class Meta:
        verbose_name = 'Отчет книговыдачи по детской библиотеке'
        verbose_name_plural = 'Отчеты книговыдачи детским библиотекам'

    def __str__(self):
        return f"{self.library}"


class AdultVisitReport(models.Model):
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Библиотека')
    cafedra = models.ForeignKey(Cafedra, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Кафедра')
    date = models.DateField(null=True, verbose_name='Дата отчета')
    qty_reg_35 = models.IntegerField(default=0, verbose_name='Новые (Молодежь 14+)')
    qty_reg_other = models.IntegerField(default=0, verbose_name='Новые (Прочие 35+)')
    qty_reg_invalid = models.IntegerField(default=0, verbose_name='Новые (Инвалиды)')
    qty_visited_35 = models.IntegerField(default=0, verbose_name='Посещение (Молодежь 14+)')
    qty_visited_other = models.IntegerField(default=0, verbose_name='Посещение (Прочие 35+)')
    qty_visited_invalids = models.IntegerField(default=0, verbose_name='Посещение (Инвалиды)')
    qty_events_35 = models.IntegerField(default=0, verbose_name='Мероприятия (Молодежь 14+)')
    qty_events_other = models.IntegerField(default=0, verbose_name='Мероприятия (Прочие 35+)')
    qty_events_invalids = models.IntegerField(default=0, verbose_name='Мероприятия (Инвалиды)')
    qty_events_out_station = models.IntegerField(default=0, verbose_name='Мероприятия (Внестационар)')
    qty_online_requests = models.IntegerField(default=0, verbose_name='Удаленные обращения')
    qty_paid = models.IntegerField(default=0, verbose_name='Платные посещения')
    note = models.TextField(blank=True, verbose_name='Примечание')

    class Meta:
        verbose_name = 'Отчет посещений по взрослой библиотеке'
        verbose_name_plural = 'Отчеты посещений взрослых библиотек'

    def __str__(self):
        return f"{self.date} {self.library}"


class AdultBookReport(models.Model):
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Библиотека')
    cafedra = models.ForeignKey(Cafedra, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Кафедра')
    date = models.DateField(null=True, verbose_name='Дата отчета')
    qty_books_14 = models.IntegerField(default=0, verbose_name='Книговыдача (14+)')
    qty_books_35 = models.IntegerField(default=0, verbose_name='Книговыдача (35+)')
    qty_books_invalid = models.IntegerField(default=0, verbose_name='Книговыдача (Инвалиды)')
    qty_books_part_opl = models.IntegerField(default=0, verbose_name='Общ.-политтич.лит-ра')
    qty_books_part_enm = models.IntegerField(default=0, verbose_name='Естеств. Науки. Медицина')
    qty_books_part_tech = models.IntegerField(default=0, verbose_name='Техника')
    qty_books_part_sh = models.IntegerField(default=0, verbose_name='Сельское хозяйство')
    qty_books_part_si = models.IntegerField(default=0, verbose_name='Спорт. Искусство')
    qty_books_part_yl = models.IntegerField(default=0, verbose_name='Языкознание. Литературоведение')
    qty_books_part_hl = models.IntegerField(default=0, verbose_name='Художественная лит-ра')
    qty_books_part_dl = models.IntegerField(default=0, verbose_name='Детская литература')
    qty_books_part_other = models.IntegerField(default=0, verbose_name='Прочие(в т.ч. журналы)')
    qty_books_part_audio = models.IntegerField(default=0, verbose_name='Аудиокниги')
    qty_books_part_krai = models.IntegerField(default=0, verbose_name='Краеведение(в том числе)')
    qty_books_reference_14 = models.IntegerField(default=0, verbose_name='Справки (14+)')
    qty_books_reference_35 = models.IntegerField(default=0, verbose_name='Справки (35+)')
    qty_books_reference_invalid = models.IntegerField(default=0, verbose_name='Справки (Инвалиды)')
    qty_books_reference_online = models.IntegerField(default=0, verbose_name='Справки (Удаленно')
    note = models.TextField(blank=True, verbose_name='Примечание')

    class Meta:
        verbose_name = 'Отчет книговыдачи по взрослой библиотеке'
        verbose_name_plural = 'Отчеты книговыдачи по взрослым библиотекам'

    def __str__(self):
        return f"{self.date} {self.library}"


