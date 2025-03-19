from collections import defaultdict

from .checks import check_data_fillings
from .report_generator import generate_all_reports_excel, generate_quarter_excel, generate_digital_month_report, \
    generate_nats_project_report
from .utils import get_book_totals, get_event_totals, get_all_visit_totals, \
    get_all_book_totals, get_all_event_totals, get_visits_totals
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import timedelta, datetime
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from .models import Event, VisitReport, BookReport
from .forms import EventForm, BookReportForm, VisitReportForm
from apps.core.models import Employee


class LoginRequiredMixin:
    login_url = "/login_home"

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required(view, login_url=cls.login_url)


class CachedViewMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return cache_page(60 * 5)(view)


def export_all_reports(request):
    user = request.user
    year = 2025
    month = int(request.GET.get('month'))
    response = generate_all_reports_excel(user, year, month)
    if response:
        return response
    else:
        return HttpResponse("Нет данных для экспорта или пользователь не связан с сотрудником.", status=404)


def export_quarter_report(request):
    year = 2025  # Текущий год
    quarter = int(request.GET.get('quarter'))  # Получаем квартал из запроса
    response = generate_quarter_excel(request.user, year, quarter)
    if response:
        return response
    else:
        return HttpResponse("Нет данных для экспорта или пользователь не связан с сотрудником.", status=404)


def export_digital_month_report(request):
    month = int(request.GET.get('month'))
    response = generate_digital_month_report(request.user, month)
    if response:
        return response
    else:
        return HttpResponse("Нет данных для экспорта или пользователь не связан с сотрудником.", status=404)


def export_nats_project_report(request):
    year = 2025  # Текущий год
    month = int(request.GET.get('month_nats'))  # Получаем месяц из запроса
    response = generate_nats_project_report(request.user, year, month)
    if response:
        return response
    else:
        return HttpResponse("Нет данных для экспорта или пользователь не связан с сотрудником.", status=404)


class DiaryView(LoginRequiredMixin, TemplateView):
    template_name = 'diary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {"parent": "Отчеты", "child": "Дневник"}
        context['visitreport'] = VisitReport.objects.all()
        context['bookreport'] = BookReport.objects.all()
        context['events'] = Event.objects.all()
        context['form'] = EventForm()
        user = self.request.user
        context['totals_visits_branch'] = get_visits_totals(user)
        context['totals_books_branch'] = get_book_totals(user)
        context['totals_event_branch'] = get_event_totals(user)
        return context


@login_required
def diary_svod(request):
    all_totals_visits = get_all_visit_totals()  # Общие итоги по всем библиотекам
    all_totals_books = get_all_book_totals()  # Общие итоги по всем библиотекам
    all_totals_events = get_all_event_totals()  # Общие итоги по всем библиотекам
    reports_fill_check = check_data_fillings()

    context = {
        'all_totals_visits': all_totals_visits,
        'all_totals_books': all_totals_books,
        'all_totals_events': all_totals_events,
        'reports_fill_check': reports_fill_check,
        'breadcrumb': {"parent": "Отчеты", "child": "Сводный отчет"}
    }

    return render(request, 'diary_svod.html', context)


class EventListView(LoginRequiredMixin, TemplateView):
    template_name = 'events/events_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {"parent": f'<a href="{reverse("diary")}"><strong>Дневник</strong></a>', "child": "Мероприятия"}
        user = self.request.user
        employee = Employee.objects.get(user=user)

        # Получаем события за последние 60 дней
        date_60_days_ago = timezone.now() - timedelta(days=60)
        events = Event.objects.filter(date__gte=date_60_days_ago, library=employee.branch).order_by('-date')

        # Подготавливаем данные для графика
        dates = []
        quantity_data = []  # Общее количество мероприятий за день
        age_14_data = []    # Участники до 14 лет
        age_35_data = []    # Участники до 35 лет
        age_other_data = [] # Участники старше 35 лет
        total_age_data = [] # Общее количество участников (линия)

        # Используем defaultdict для агрегации данных по дням
        day_count = defaultdict(lambda: {
            'quantity': 0,  # Количество мероприятий
            'age_14': 0,    # Участники до 14 лет
            'age_35': 0,    # Участники до 35 лет
            'age_other': 0, # Участники старше 35 лет
            'online': 0,    # Онлайн-участники
            'out_of_station': 0  # Участники вне стационара
        })

        for event in events:
            # Используем объект datetime.date для группировки и сортировки
            day_key = event.date  # event.date уже является объектом datetime.date
            day_count[day_key]['quantity'] += event.quantity
            day_count[day_key]['age_14'] += event.age_14
            day_count[day_key]['age_35'] += event.age_35
            day_count[day_key]['age_other'] += event.age_other
            day_count[day_key]['online'] += event.online
            day_count[day_key]['out_of_station'] += event.out_of_station

        # Сортируем данные по дате (по возрастанию)
        sorted_days = sorted(day_count.keys())

        for day in sorted_days:
            counts = day_count[day]
            dates.append(day.strftime('%d.%m.%Y'))  # Преобразуем дату в строку для графика
            quantity_data.append(counts['quantity'])
            age_14_data.append(counts['age_14'])
            age_35_data.append(counts['age_35'])
            age_other_data.append(counts['age_other'])
            # Общее количество участников: age_14 + age_35 + age_other + online + out_of_station
            total_age_data.append(counts['age_14'] + counts['age_35'] + counts['age_other'] + counts['online'] + counts['out_of_station'])

        # Логируем данные для отладки
        print("Dates:", dates)
        print("Quantity Data:", quantity_data)
        print("Age 14 Data:", age_14_data)
        print("Age 35 Data:", age_35_data)
        print("Age Other Data:", age_other_data)
        print("Total Age Data:", total_age_data)

        context['events'] = events
        context['dates'] = dates
        context['quantity_data'] = quantity_data
        context['age_14_data'] = age_14_data
        context['age_35_data'] = age_35_data
        context['age_other_data'] = age_other_data
        context['total_age_data'] = total_age_data

        context['form'] = EventForm(user=user)

        return context


class EventCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = EventForm(user=request.user)  # Создаем пустую форму
        breadcrumb = {"parent": f'<a href="{reverse("diary")}"><strong>Дневник</strong></a>', "child": "Мероприятия"}
        return render(request, 'events/event_form.html', {'form': form, 'breadcrumb': breadcrumb})

    def post(self, request):
        form = EventForm(request.POST, user=request.user)
        breadcrumb = {"parent": f'<a href="{reverse("diary")}"><strong>Дневник</strong></a>', "child": "Мероприятия"}
        if form.is_valid():
            event = form.save(commit=False)  # Не сохраняем объект сразу
            employee = Employee.objects.get(user=request.user)
            event.library = employee.branch  # Устанавливаем библиотеку
            event.save()  # Сохраняем объект
            return redirect(reverse_lazy('events_list'))
        return render(request, 'events/event_form.html', {'form': form, 'breadcrumb': breadcrumb})


class EventUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        event_instance = get_object_or_404(Event, id=id)  # Получаем объект события по id
        form = EventForm(instance=event_instance, user=request.user)  # Создаем форму с текущими данными события
        breadcrumb = {"parent": f'<a href="{reverse("diary")}"><strong>Дневник</strong></a>', "child": "Мероприятия"}
        return render(request, 'events/event_form.html', {'form': form, 'breadcrumb': breadcrumb})

    def post(self, request, id):
        event_instance = get_object_or_404(Event, id=id)
        form = EventForm(request.POST, instance=event_instance, user=request.user)
        breadcrumb = {"parent": f'<a href="{reverse("diary")}"><strong>Дневник</strong></a>', "child": "Мероприятия"}
        if form.is_valid():
            event = form.save(commit=False)  # Не сохраняем объект сразу
            employee = Employee.objects.get(user=request.user)
            event.library = employee.branch  # Устанавливаем библиотеку
            event.save()  # Сохраняем объект
            return redirect(reverse_lazy('events_list'))
        return render(request, 'events/event_form.html', {'form': form, 'breadcrumb': breadcrumb})


class EventDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        event = get_object_or_404(Event, id=id)
        # Добавьте проверку прав, если нужно (например, что только автор может удалять)
        # if event.author != request.user:
        #     return HttpResponseForbidden("У вас нет прав на удаление этого мероприятия.")
        event.delete()
        return redirect(reverse_lazy('events_list')) # Перенаправляем на список мероприятий


class VisitReportListView(LoginRequiredMixin, ListView):
    model = VisitReport
    template_name = 'visits/visits_list.html'
    context_object_name = 'visits'

    def get_queryset(self):
        user = self.request.user
        employee = Employee.objects.get(user=user)
        date_60_days_ago = timezone.now() - timedelta(days=60)
        return VisitReport.objects.filter(date__gte=date_60_days_ago, library=employee.branch).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            "parent": f'<a href="{reverse("diary")}"><strong>Дневник</strong></a>',  # Добавляем ссылку на Дневник
            "child": "Регистрация/Посещения"
        }
        visits = self.get_queryset()

        # Подготавливаем данные для графика
        dates = []
        qty_reg_14_data = []
        qty_reg_15_35_data = []
        qty_reg_other_data = []
        qty_reg_invalid_data = []
        qty_visited_14_data = []
        qty_visited_15_35_data = []
        qty_visited_other_data = []
        qty_visited_invalids_data = []
        total_reg_data = []
        total_visited_data = []

        day_count = defaultdict(lambda: {
            'qty_reg_14': 0,
            'qty_reg_15_35': 0,
            'qty_reg_other': 0,
            'qty_reg_invalid': 0,
            'qty_visited_14': 0,
            'qty_visited_15_35': 0,
            'qty_visited_other': 0,
            'qty_visited_invalids': 0,
        })

        for visit in visits:
            day_str = visit.date.strftime('%d.%m.%Y')
            day_count[day_str]['qty_reg_14'] += visit.qty_reg_14
            day_count[day_str]['qty_reg_15_35'] += visit.qty_reg_15_35
            day_count[day_str]['qty_reg_other'] += visit.qty_reg_other
            day_count[day_str]['qty_reg_invalid'] += visit.qty_reg_invalid

            day_count[day_str]['qty_visited_14'] += visit.qty_visited_14
            day_count[day_str]['qty_visited_15_35'] += visit.qty_visited_15_35
            day_count[day_str]['qty_visited_other'] += visit.qty_visited_other
            day_count[day_str]['qty_visited_invalids'] += visit.qty_visited_invalids

        for date, counts in sorted(day_count.items()):
            dates.append(date)
            qty_reg_14_data.append(counts['qty_reg_14'])
            qty_reg_15_35_data.append(counts['qty_reg_15_35'])
            qty_reg_other_data.append(counts['qty_reg_other'])
            qty_reg_invalid_data.append(counts['qty_reg_invalid'])
            qty_visited_14_data.append(counts['qty_visited_14'])
            qty_visited_15_35_data.append(counts['qty_visited_15_35'])
            qty_visited_other_data.append(counts['qty_visited_other'])
            qty_visited_invalids_data.append(counts['qty_visited_invalids'])
            total_reg_data.append(counts['qty_reg_14'] + counts['qty_reg_15_35'] + counts['qty_reg_other'] +
                                  counts['qty_reg_invalid'])
            total_visited_data.append(counts['qty_visited_14'] + counts['qty_visited_15_35'] +
                                      counts['qty_visited_other'] + counts['qty_visited_invalids'])

        # Логируем данные для отладки
        print("Dates:", dates)
        print("Qty Reg 14 Data:", qty_reg_14_data)
        print("Qty Reg 15_35 Data:", qty_reg_15_35_data)
        print("Qty Reg Other Data:", qty_reg_other_data)
        print("Qty Reg Invalid Data:", qty_reg_invalid_data)
        print("Qty Visited 15_35 Data:", qty_visited_15_35_data)
        print("Qty Visited Other Data:", qty_visited_other_data)
        print("Qty Visited Invalids Data:", qty_visited_invalids_data)
        print("Total Reg Data:", total_reg_data)
        print("Total Visited Data:", total_visited_data)

        context['dates'] = dates
        context['qty_reg_14_data'] = qty_reg_14_data
        context['qty_reg_15_35_data'] = qty_reg_15_35_data
        context['qty_reg_other_data'] = qty_reg_other_data
        context['qty_reg_invalid_data'] = qty_reg_invalid_data
        context['qty_visited_15_35_data'] = qty_visited_15_35_data
        context['qty_visited_other_data'] = qty_visited_other_data
        context['qty_visited_invalids_data'] = qty_visited_invalids_data
        context['total_reg_data'] = total_reg_data
        context['total_visited_data'] = total_visited_data

        return context


class VisitReportCreateView(LoginRequiredMixin, CreateView):
    model = VisitReport
    form_class = VisitReportForm
    template_name = 'visits/visit_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib
        context['breadcrumb'] = {"parent": f'<a href="{reverse("diary")}"><strong>Дневник</strong></a>', "child": "Добавить Посещение"}
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('visits_list')


class VisitReportUpdateView(LoginRequiredMixin, UpdateView):
    model = VisitReport
    form_class = VisitReportForm
    template_name = 'visits/visit_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib
        context['breadcrumb'] = {"parent": f'<a href="{reverse("diary")}"><strong>Дневник</strong></a>', "child": "Редактировать Посещение"}
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('visits_list')


class VisitDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        visit = get_object_or_404(VisitReport, id=id)
        # Добавьте проверку прав, если нужно (например, что только автор может удалять)
        # if event.author != request.user:
        #     return HttpResponseForbidden("У вас нет прав на удаление этого мероприятия.")
        visit.delete()
        return redirect(reverse_lazy('visits_list')) # Перенаправляем на список мероприятий


class BookReportListView(LoginRequiredMixin, ListView):
    model = BookReport
    template_name = 'books/books_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        user = self.request.user
        employee = Employee.objects.get(user=user)
        date_60_days_ago = timezone.now() - timedelta(days=60)
        return BookReport.objects.filter(date__gte=date_60_days_ago, library=employee.branch).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib
        context['breadcrumb'] = {"parent": f'<a href="{reverse("diary")}"><strong>Дневник</strong></a>', "child": "Книговыдача"}
        reports = self.get_queryset()

        # Подготавливаем данные для графика
        dates = []
        qty_books_14_data = []
        qty_books_15_35_data = []
        qty_books_invalid_data = []
        qty_books_neb_data = []
        qty_books_prlib_data = []
        qty_books_litres_data = []
        qty_books_consultant_data = []
        qty_books_part_opl_data = []
        qty_books_part_enm_data = []
        qty_books_part_tech_data = []
        qty_books_part_sh_data = []
        qty_books_part_si_data = []
        qty_books_part_yl_data = []
        qty_books_part_hl_data = []
        qty_books_part_dl_data = []
        qty_books_part_other_data = []
        qty_books_part_audio_data = []
        qty_books_part_krai_data = []
        qty_books_reference_14_data = []
        qty_books_reference_35_data = []
        qty_books_reference_invalid_data = []
        qty_books_reference_online_data = []
        total_books_data = []
        total_references_data = []

        day_count = defaultdict(lambda: {
            'qty_books_14': 0,
            'qty_books_15_35': 0,
            'qty_books_invalid': 0,
            'qty_books_neb': 0,
            'qty_books_prlib': 0,
            'qty_books_litres': 0,
            'qty_books_consultant': 0,
            'qty_books_part_opl': 0,
            'qty_books_part_enm': 0,
            'qty_books_part_tech': 0,
            'qty_books_part_sh': 0,
            'qty_books_part_si': 0,
            'qty_books_part_yl': 0,
            'qty_books_part_hl': 0,
            'qty_books_part_dl': 0,
            'qty_books_part_other': 0,
            'qty_books_part_audio': 0,
            'qty_books_part_krai': 0,
            'qty_books_reference_14': 0,
            'qty_books_reference_35': 0,
            'qty_books_reference_invalid': 0,
            'qty_books_reference_online': 0,
        })

        for report in reports:
            day_str = report.date.strftime('%d.%m.%Y')
            day_count[day_str]['qty_books_14'] += report.qty_books_14
            day_count[day_str]['qty_books_15_35'] += report.qty_books_15_35
            day_count[day_str]['qty_books_invalid'] += report.qty_books_invalid
            day_count[day_str]['qty_books_neb'] += report.qty_books_neb
            day_count[day_str]['qty_books_prlib'] += report.qty_books_prlib
            day_count[day_str]['qty_books_litres'] += report.qty_books_litres
            day_count[day_str]['qty_books_consultant'] += report.qty_books_consultant
            day_count[day_str]['qty_books_part_opl'] += report.qty_books_part_opl
            day_count[day_str]['qty_books_part_enm'] += report.qty_books_part_enm
            day_count[day_str]['qty_books_part_tech'] += report.qty_books_part_tech
            day_count[day_str]['qty_books_part_sh'] += report.qty_books_part_sh
            day_count[day_str]['qty_books_part_si'] += report.qty_books_part_si
            day_count[day_str]['qty_books_part_yl'] += report.qty_books_part_yl
            day_count[day_str]['qty_books_part_hl'] += report.qty_books_part_hl
            day_count[day_str]['qty_books_part_dl'] += report.qty_books_part_dl
            day_count[day_str]['qty_books_part_other'] += report.qty_books_part_other
            day_count[day_str]['qty_books_part_audio'] += report.qty_books_part_audio
            day_count[day_str]['qty_books_part_krai'] += report.qty_books_part_krai
            day_count[day_str]['qty_books_reference_14'] += report.qty_books_reference_14
            day_count[day_str]['qty_books_reference_35'] += report.qty_books_reference_35
            day_count[day_str]['qty_books_reference_invalid'] += report.qty_books_reference_invalid
            day_count[day_str]['qty_books_reference_online'] += report.qty_books_reference_online

        for date, counts in sorted(day_count.items()):
            dates.append(date)
            qty_books_14_data.append(counts['qty_books_14'])
            qty_books_15_35_data.append(counts['qty_books_15_35'])
            qty_books_invalid_data.append(counts['qty_books_invalid'])
            qty_books_neb_data.append(counts['qty_books_neb'])
            qty_books_prlib_data.append(counts['qty_books_prlib'])
            qty_books_litres_data.append(counts['qty_books_litres'])
            qty_books_consultant_data.append(counts['qty_books_consultant'])
            qty_books_part_opl_data.append(counts['qty_books_part_opl'])
            qty_books_part_enm_data.append(counts['qty_books_part_enm'])
            qty_books_part_tech_data.append(counts['qty_books_part_tech'])
            qty_books_part_sh_data.append(counts['qty_books_part_sh'])
            qty_books_part_si_data.append(counts['qty_books_part_si'])
            qty_books_part_yl_data.append(counts['qty_books_part_yl'])
            qty_books_part_hl_data.append(counts['qty_books_part_hl'])
            qty_books_part_dl_data.append(counts['qty_books_part_dl'])
            qty_books_part_other_data.append(counts['qty_books_part_other'])
            qty_books_part_audio_data.append(counts['qty_books_part_audio'])
            qty_books_part_krai_data.append(counts['qty_books_part_krai'])
            qty_books_reference_14_data.append(counts['qty_books_reference_14'])
            qty_books_reference_35_data.append(counts['qty_books_reference_35'])
            qty_books_reference_invalid_data.append(counts['qty_books_reference_invalid'])
            qty_books_reference_online_data.append(counts['qty_books_reference_online'])
            total_books_data.append(
                counts['qty_books_14'] + counts['qty_books_15_35'] + counts['qty_books_invalid'] + counts['qty_books_neb']
                + counts['qty_books_prlib']+ counts['qty_books_litres']+ counts['qty_books_consultant']
            )
            total_references_data.append(
                counts['qty_books_reference_14'] + counts['qty_books_reference_35'] +
                counts['qty_books_reference_invalid'] + counts['qty_books_reference_online']
            )

        context['dates'] = dates
        context['qty_books_14_data'] = qty_books_14_data
        context['qty_books_15_35_data'] = qty_books_15_35_data
        context['qty_books_invalid_data'] = qty_books_invalid_data
        context['qty_books_part_opl_data'] = qty_books_part_opl_data
        context['qty_books_part_enm_data'] = qty_books_part_enm_data
        context['qty_books_part_tech_data'] = qty_books_part_tech_data
        context['qty_books_part_sh_data'] = qty_books_part_sh_data
        context['qty_books_part_si_data'] = qty_books_part_si_data
        context['qty_books_part_yl_data'] = qty_books_part_yl_data
        context['qty_books_part_hl_data'] = qty_books_part_hl_data
        context['qty_books_part_dl_data'] = qty_books_part_dl_data
        context['qty_books_part_other_data'] = qty_books_part_other_data
        context['qty_books_part_audio_data'] = qty_books_part_audio_data
        context['qty_books_part_krai_data'] = qty_books_part_krai_data
        context['qty_books_reference_14_data'] = qty_books_reference_14_data
        context['qty_books_reference_35_data'] = qty_books_reference_35_data
        context['qty_books_reference_invalid_data'] = qty_books_reference_invalid_data
        context['qty_books_reference_online_data'] = qty_books_reference_online_data
        context['total_books_data'] = total_books_data
        context['total_references_data'] = total_references_data

        return context


class BookReportCreateView(LoginRequiredMixin, CreateView):
    model = BookReport
    form_class = BookReportForm
    template_name = 'books/book_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib  # Передаем статус модельной библиотеки в контекст
        context['breadcrumb'] = {"parent": f'<a href="{reverse("diary")}"><strong>Дневник</strong></a>', "child": "Добавить книговыдачу"}
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['mod_lib'] = Employee.objects.get(user=self.request.user).branch.mod_lib  # Передаем статус модельной библиотеки в форму
        return kwargs

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('books_list')


class BookReportUpdateView(LoginRequiredMixin, UpdateView):
    model = BookReport
    form_class = BookReportForm
    template_name = 'books/book_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib
        context['breadcrumb'] = {"parent": f'<a href="{reverse("diary")}"><strong>Дневник</strong></a>', "child": "Редактировать книговыдачу"}
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['mod_lib'] = Employee.objects.get(
            user=self.request.user).branch.mod_lib  # Передаем статус модельной библиотеки в форму
        return kwargs

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('books_list')


class BookReportDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = get_object_or_404(BookReport, id=id)
        # Добавьте проверку прав, если нужно (например, что только автор может удалять)
        # if event.author != request.user:
        #     return HttpResponseForbidden("У вас нет прав на удаление этого мероприятия.")
        book.delete()
        return redirect(reverse_lazy('books_list')) # Перенаправляем на список мероприятий