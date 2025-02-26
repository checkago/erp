from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.core.models import Branch, Cafedra


#Массовые мероприятия
class Event(models.Model):
    
    DN = 'Досуговое направление'
    DNN = 'Духовно-нравственное'
    EST = 'Эстетическое направление'
    IPN = 'Историко-патриотическое направление'
    KR = 'Краеведение'
    NPN = 'Научно-популярное направление'
    PPNTAT = 'Профилактика правонарушений, в т.ч. наркомании, токсикомании, алкоголизма, табакокурения'
    PSPN = 'Профилактика суицидального поведения несовершеннолетних'
    PTE = 'Профилактика терроризма и экстремизма'
    PO = 'Профориентация'
    TECH = 'Техника'
    SKAM = 'Социальная и культурная адаптация мигрантов'
    UMMS = 'Укрепление межнационального и межрелигиозного согласия'
    UOZ = 'Укрепление общественного здоровья'
    EP = 'Экологическое просвещение'
    FTS = 'Фотосессия'
    SEM = 'Семинар'

    direction_CHOICES = (
        (DN, 'Досуговое направление'),
        (DNN, 'Духовно-нравственное'),
        (EST, 'Эстетическое направление'),
        (IPN, 'Историко-патриотическое направление'),
        (KR, 'Краеведение'),
        (NPN, 'Научно-популярное направление'),
        (PPNTAT, 'Профилактика правонарушений, в т.ч. наркомании, токсикомании, алкоголизма, табакокурения'),
        (PSPN, 'Профилактика суицидального поведения несовершеннолетних'),
        (PTE, 'Профилактика терроризма и экстремизма'),
        (PO, 'Профориентация'),
        (TECH, 'Техника'),
        (SKAM, 'Социальная и культурная адаптация мигрантов'),
        (UMMS, 'Укрепление межнационального и межрелигиозного согласия'),
        (UOZ, 'Укрепление общественного здоровья'),
        (EP, 'Экологическое просвещение'),
        (FTS, 'Фотосессия'),
        (SEM, 'Семинар')
    )

    KRUJKI = 'Кружки'
    AD = 'Активное долголетие'
    OTHER = 'Прочие'

    age_CHOICES = (
        (KRUJKI, 'Кружки'),
        (AD, 'Активное долголетие'),
        (OTHER, 'Прочие'),
    )
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='events', verbose_name='Библиотека')
    cafedra = models.ForeignKey(Cafedra, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Кафедра')
    name = models.CharField(max_length=250, verbose_name='Название мероприятия')
    date = models.DateField(verbose_name='Дата проведения')
    direction = models.CharField(max_length=150, choices=direction_CHOICES, default=IPN,
                                  verbose_name='Направление')
    quantity = models.IntegerField(default=1, verbose_name='Количество мероприятий')
    age_14 = models.IntegerField(default=0, verbose_name='До 14')
    age_35 = models.IntegerField(default=0, verbose_name='До 30')
    age_other = models.IntegerField(default=0, verbose_name='После 30 и другие')
    invalids = models.IntegerField(default=0, verbose_name='Инвалиды (из общего числа)')
    pensioners = models.IntegerField(default=0, verbose_name='Пенсионеры (из общего числа)')
    out_of_station = models.IntegerField(default=0, verbose_name='Внестационар')
    online = models.IntegerField(default=0, verbose_name='Удаленно')
    as_part = models.CharField(max_length=150, choices=age_CHOICES, default=KRUJKI,
                                 verbose_name='В рамках')
    paid = models.BooleanField(default=False, blank=True, verbose_name='Платное')
    note = models.TextField(verbose_name='Примечание', blank=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Массовые мероприятия'

    def __str__(self):
        return f"{self.date} {self.name} {self.direction}"


class VisitReport(models.Model):
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='visitreports', verbose_name='Библиотека')
    cafedra = models.ForeignKey(Cafedra, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Кафедра')
    date = models.DateField(null=True, verbose_name='Дата отчета')
    qty_reg_14 = models.IntegerField(default=0, verbose_name='Новые (До 14)')
    qty_reg_15_35 = models.IntegerField(default=0, verbose_name='Новые (Молодежь 14-30)')
    qty_reg_other = models.IntegerField(default=0, verbose_name='Новые (Прочие 30+)')
    qty_reg_invalid = models.IntegerField(default=0, verbose_name='Новые (Инвалиды (из общего числа))')
    qty_reg_pensioners = models.IntegerField(default=0, verbose_name='Новые (Пенсионеры (из общего числа))')
    qty_reg_out_of_station = models.IntegerField(default=0, verbose_name='Новые (Внестационар)')
    qty_reg_prlib = models.IntegerField(default=0, verbose_name='Новые (Президентская)')
    qty_reg_litres = models.IntegerField(default=0, verbose_name='Новые (Литрес)')
    qty_visited_14 = models.IntegerField(default=0, verbose_name='Посещение (До 14)')
    qty_visited_15_35 = models.IntegerField(default=0, verbose_name='Посещение (Молодежь 15-30)')
    qty_visited_other = models.IntegerField(default=0, verbose_name='Посещение (Прочие 30+)')
    qty_visited_invalids = models.IntegerField(default=0, verbose_name='Посещение (Инвалиды (из общего числа))')
    qty_visited_pensioners = models.IntegerField(default=0, verbose_name='Посещение (Пенсионеры (из общего числа))')
    qty_visited_out_station = models.IntegerField(default=0, verbose_name='Посещение (Внестационар)')
    qty_visited_online = models.IntegerField(default=0, verbose_name='Посещение (Удаленно)')
    qty_visited_prlib = models.IntegerField(default=0, verbose_name='Посещение (Президентская)')
    qty_visited_litres = models.IntegerField(default=0, verbose_name='Посещение (Литрес)')
    note = models.TextField(blank=True, verbose_name='Примечание')

    class Meta:
        verbose_name = 'Отчет посещений по библиотеке'
        verbose_name_plural = 'Отчеты посещений по библиотекам'

    def __str__(self):
        return f"{self.library}"


class BookReport(models.Model):
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='bookreports', verbose_name='Библиотека')
    cafedra = models.ForeignKey(Cafedra, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Кафедра')
    date = models.DateField(null=True, verbose_name='Дата отчета')
    qty_books_14 = models.IntegerField(default=0, verbose_name='Книговыдача (До 14)')
    qty_books_15_35 = models.IntegerField(default=0, verbose_name='Книговыдача (14-30)')
    qty_books_other = models.IntegerField(default=0, verbose_name='Книговыдача (Прочие 30+)')
    qty_books_invalid = models.IntegerField(default=0, verbose_name='Книговыдача (Инвалиды (из общего числа))')
    qty_books_out_of_station = models.IntegerField(default=0, verbose_name='Книговыдача (Внестационар)')
    qty_books_neb = models.IntegerField(default=0, verbose_name='Книговыдача (НЭБ)')
    qty_books_prlib = models.IntegerField(default=0, verbose_name='Книговыдача (Президентская)')
    qty_books_litres = models.IntegerField(default=0, verbose_name='Книговыдача (Литрес)')
    qty_books_consultant = models.IntegerField(default=0, verbose_name='Книговыдача (Консультант+)')
    qty_books_local_library = models.IntegerField(default=0, verbose_name='Книговыдача (Локальная биб.)')
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
    qty_books_part_krai = models.IntegerField(default=0, verbose_name='Краеведение(из общего числа)')
    qty_books_reference_do_14 = models.IntegerField(default=0, verbose_name='Справки (До 14)')
    qty_books_reference_14 = models.IntegerField(default=0, verbose_name='Справки (14-30)')
    qty_books_reference_35 = models.IntegerField(default=0, verbose_name='Справки (30+)')
    qty_books_reference_other = models.IntegerField(default=0, verbose_name='Справки (Прочие)')
    qty_books_reference_invalid = models.IntegerField(default=0, verbose_name='Справки (Инвалиды (из общего числа))')
    qty_books_reference_online = models.IntegerField(default=0, verbose_name='Справки (Удаленно')
    note = models.TextField(blank=True, verbose_name='Примечание')


    class Meta:
        verbose_name = 'Отчет книговыдачи по библиотеке'
        verbose_name_plural = 'Отчеты книговыдачи библиотекам'

    def __str__(self):
        return f"{self.library}"


class VisitPlan(models.Model):
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        verbose_name='Год'
    )
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')
    total_visits = models.IntegerField(verbose_name='Количество')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'library', 'total_visits'],
                name='unique_year_library_total_visits'
            )
        ]
        verbose_name = 'План посещаемости год'
        verbose_name_plural = 'Планы посещаемости на год'

    def __str__(self):
        return f"{self.library} ({self.year})"


class BookPlan(models.Model):
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        verbose_name='Год'
    )
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')
    total_books = models.IntegerField(verbose_name='Количество')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'library', 'total_books'],
                name='unique_year_library_total_books'
            )
        ]
        verbose_name = 'План книговыдачи на год'
        verbose_name_plural = 'Планы книговыдачи на год'

    def __str__(self):
        return f"{self.library} ({self.year})"


class EventsPlan(models.Model):
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        verbose_name='Год'
    )
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')
    total_events = models.IntegerField(verbose_name='Количество')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'library', 'total_events'],
                name='unique_year_library_total_events'
            )
        ]
        verbose_name = 'План мероприятий на год'
        verbose_name_plural = 'Планы мероприятий на год'

    def __str__(self):
        return f"{self.library} ({self.year})"


class RegsPlan(models.Model):
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        verbose_name='Год'
    )
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')
    total_regs = models.IntegerField(verbose_name='Количество')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'library', 'total_regs'],
                name='unique_year_library_total_regs'
            )
        ]
        verbose_name = 'План регистраций на год'
        verbose_name_plural = 'Планы регистраций на год'

    def __str__(self):
        return f"{self.library} ({self.year})"


class RegsFirstData(models.Model):
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')
    data = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Начальные данные по регистрациям'
        verbose_name_plural = 'Начальные данные по регистрациям'

    def __str__(self):
        return f"{self.library}"


class VisitsFirstData(models.Model):
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')
    data = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Начальные данные по посещениям'
        verbose_name_plural = 'Начальные данные по посещениям'

    def __str__(self):
        return f"{self.library}"


class EventsFirstData(models.Model):
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')
    data = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Начальные данные по мероприятиям'
        verbose_name_plural = 'Начальные данные по мероприятиям'

    def __str__(self):
        return f"{self.library}"


class BooksFirstData(models.Model):
    library = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')
    data = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Начальные данные по книговыдаче'
        verbose_name_plural = 'Начальные данные по книговыдаче'

    def __str__(self):
        return f"{self.library}"