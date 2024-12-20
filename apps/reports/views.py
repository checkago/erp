from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import timedelta, datetime
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from .models import Event, AdultVisitReport, AdultBookReport, ChildVisitReport, ChildBookReport
from .forms import EventForm, AdultBookReportForm, AdultVisitReportForm, ChildVisitReportForm, ChildBookReportForm
from apps.core.models import Employee


class LoginRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required(view)


class CachedViewMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return cache_page(60 * 5)(view)


class DiaryView(LoginRequiredMixin, TemplateView):
    template_name = 'diary.html'  # Укажите путь к вашему шаблону

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {"parent": "Отчеты", "child": "Дневник"}
        context['adultvisitreport'] = AdultVisitReport.objects.all()
        context['adultvisitreport'] = AdultBookReport.objects.all()
        context['childvisitreport'] = ChildVisitReport.objects.all()
        context['childvisitreport'] = ChildBookReport.objects.all()
        context['events'] = Event.objects.all()
        context['form'] = EventForm()
        return context


class EventListView(LoginRequiredMixin, TemplateView):
    template_name = 'events/events_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {"parent": "Дневник", "child": "Мероприятия"}
        user = self.request.user
        employee = Employee.objects.get(user=user)

        # Получаем события за последние 15 дней
        date_15_days_ago = timezone.now() - timedelta(days=15)
        events = Event.objects.filter(date__gte=date_15_days_ago, library=employee.branch).order_by('-date')[:15]

        # Подготавливаем данные для графика
        dates = []
        quantity_data = []
        age_14_data = []
        age_35_data = []
        age_other_data = []
        total_age_data = []

        day_count = defaultdict(lambda: {
            'quantity': 0,
            'age_14': 0,
            'age_35': 0,
            'age_other': 0
        })

        for event in events:
            day_str = event.date.strftime('%d.%m.%Y')
            day_count[day_str]['quantity'] += event.quantity
            day_count[day_str]['age_14'] += event.age_14
            day_count[day_str]['age_35'] += event.age_35
            day_count[day_str]['age_other'] += event.age_other

        for date, counts in sorted(day_count.items()):
            dates.append(date)
            quantity_data.append(counts['quantity'])
            age_14_data.append(counts['age_14'])
            age_35_data.append(counts['age_35'])
            age_other_data.append(counts['age_other'])
            total_age_data.append(counts['age_14'] + counts['age_35'] + counts['age_other'])

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
        return render(request, 'events/event_form.html', {'form': form})

    def post(self, request):
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)  # Не сохраняем объект сразу
            employee = Employee.objects.get(user=request.user)
            event.library = employee.branch  # Устанавливаем библиотеку
            event.save()  # Сохраняем объект
            return redirect(reverse_lazy('events_list'))
        return render(request, 'events/event_form.html', {'form': form})


class EventUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        event_instance = get_object_or_404(Event, id=id)  # Получаем объект события по id
        form = EventForm(instance=event_instance, user=request.user)  # Создаем форму с текущими данными события
        return render(request, 'events/event_form.html', {'form': form})

    def post(self, request, id):
        event_instance = get_object_or_404(Event, id=id)
        form = EventForm(request.POST, instance=event_instance, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)  # Не сохраняем объект сразу
            employee = Employee.objects.get(user=request.user)
            event.library = employee.branch  # Устанавливаем библиотеку
            event.save()  # Сохраняем объект
            return redirect(reverse_lazy('events_list'))
        return render(request, 'events/event_form.html', {'form': form})


class AdultVisitReportListView(LoginRequiredMixin, ListView):
    model = AdultVisitReport
    template_name = 'adult/adultvisits_list.html'
    context_object_name = 'visits'

    def get_queryset(self):
        user = self.request.user
        employee = Employee.objects.get(user=user)
        return AdultVisitReport.objects.filter(library=employee.branch).order_by('-date')[:15]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {"parent": "Посещения", "child": "Взрослая"}
        visits = self.get_queryset()

        # Подготавливаем данные для графика
        dates = []
        qty_reg_35_data = []
        qty_reg_other_data = []
        qty_reg_invalid_data = []
        qty_visited_35_data = []
        qty_visited_other_data = []
        qty_visited_invalids_data = []
        qty_events_35_data = []
        qty_events_other_data = []
        qty_events_invalids_data = []
        total_reg_data = []
        total_visited_data = []
        total_events_data = []

        day_count = defaultdict(lambda: {
            'qty_reg_35': 0,
            'qty_reg_other': 0,
            'qty_reg_invalid': 0,
            'qty_visited_35': 0,
            'qty_visited_other': 0,
            'qty_visited_invalids': 0,
            'qty_events_35': 0,
            'qty_events_other': 0,
            'qty_events_invalids': 0,
        })

        for visit in visits:
            day_str = visit.date.strftime('%d.%m.%Y')
            day_count[day_str]['qty_reg_35'] += visit.qty_reg_35
            day_count[day_str]['qty_reg_other'] += visit.qty_reg_other
            day_count[day_str]['qty_reg_invalid'] += visit.qty_reg_invalid
            day_count[day_str]['qty_visited_35'] += visit.qty_visited_35
            day_count[day_str]['qty_visited_other'] += visit.qty_visited_other
            day_count[day_str]['qty_visited_invalids'] += visit.qty_visited_invalids
            day_count[day_str]['qty_events_35'] += visit.qty_events_35
            day_count[day_str]['qty_events_other'] += visit.qty_events_other
            day_count[day_str]['qty_events_invalids'] += visit.qty_events_invalids

        for date, counts in sorted(day_count.items()):
            dates.append(date)
            qty_reg_35_data.append(counts['qty_reg_35'])
            qty_reg_other_data.append(counts['qty_reg_other'])
            qty_reg_invalid_data.append(counts['qty_reg_invalid'])
            qty_visited_35_data.append(counts['qty_visited_35'])
            qty_visited_other_data.append(counts['qty_visited_other'])
            qty_visited_invalids_data.append(counts['qty_visited_invalids'])
            qty_events_35_data.append(counts['qty_events_35'])
            qty_events_other_data.append(counts['qty_events_other'])
            qty_events_invalids_data.append(counts['qty_events_invalids'])
            total_reg_data.append(counts['qty_reg_35'] + counts['qty_reg_other'] + counts['qty_reg_invalid'])
            total_visited_data.append(counts['qty_visited_35'] + counts['qty_visited_other'] + counts['qty_visited_invalids'])
            total_events_data.append(counts['qty_events_35'] + counts['qty_events_other'] + counts['qty_events_invalids'])

        # Логируем данные для отладки
        print("Dates:", dates)
        print("Qty Reg 35 Data:", qty_reg_35_data)
        print("Qty Reg Other Data:", qty_reg_other_data)
        print("Qty Reg Invalid Data:", qty_reg_invalid_data)
        print("Qty Visited 35 Data:", qty_visited_35_data)
        print("Qty Visited Other Data:", qty_visited_other_data)
        print("Qty Visited Invalids Data:", qty_visited_invalids_data)
        print("Qty Events 35 Data:", qty_events_35_data)
        print("Qty Events Other Data:", qty_events_other_data)
        print("Qty Events Invalids Data:", qty_events_invalids_data)
        print("Total Reg Data:", total_reg_data)
        print("Total Visited Data:", total_visited_data)
        print("Total Events Data:", total_events_data)

        context['dates'] = dates
        context['qty_reg_35_data'] = qty_reg_35_data
        context['qty_reg_other_data'] = qty_reg_other_data
        context['qty_reg_invalid_data'] = qty_reg_invalid_data
        context['qty_visited_35_data'] = qty_visited_35_data
        context['qty_visited_other_data'] = qty_visited_other_data
        context['qty_visited_invalids_data'] = qty_visited_invalids_data
        context['qty_events_35_data'] = qty_events_35_data
        context['qty_events_other_data'] = qty_events_other_data
        context['qty_events_invalids_data'] = qty_events_invalids_data
        context['total_reg_data'] = total_reg_data
        context['total_visited_data'] = total_visited_data
        context['total_events_data'] = total_events_data

        return context


class AdultVisitReportCreateView(LoginRequiredMixin, CreateView):
    model = AdultVisitReport
    form_class = AdultVisitReportForm
    template_name = 'adult/adult_visit_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('adult_visits_list')


class AdultVisitReportUpdateView(LoginRequiredMixin, UpdateView):
    model = AdultVisitReport
    form_class = AdultVisitReportForm
    template_name = 'adult/adult_visit_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('adult_visits_list')


class AdultBookReportListView(LoginRequiredMixin, ListView):
    model = AdultBookReport
    template_name = 'adult/adultbooks_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        user = self.request.user
        employee = Employee.objects.get(user=user)

        return AdultBookReport.objects.filter(library=employee.branch).order_by('-date')[:15]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib
        context['breadcrumb'] = {"parent": "Книговыдача", "child": "Взрослая"}
        reports = self.get_queryset()

        # Подготавливаем данные для графика
        dates = []
        qty_books_14_data = []
        qty_books_35_data = []
        qty_books_invalid_data = []
        qty_books_neb_data = []
        qty_books_prlib_data = []
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
            'qty_books_35': 0,
            'qty_books_invalid': 0,
            'qty_books_neb': 0,
            'qty_books_prlib': 0,
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
            day_count[day_str]['qty_books_35'] += report.qty_books_35
            day_count[day_str]['qty_books_invalid'] += report.qty_books_invalid
            day_count[day_str]['qty_books_neb'] += report.qty_books_neb
            day_count[day_str]['qty_books_prlib'] += report.qty_books_prlib
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
            qty_books_35_data.append(counts['qty_books_35'])
            qty_books_invalid_data.append(counts['qty_books_invalid'])
            qty_books_neb_data.append(counts['qty_books_neb'])
            qty_books_prlib_data.append(counts['qty_books_prlib'])
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
                counts['qty_books_14'] + counts['qty_books_35'] + counts['qty_books_invalid'] + counts['qty_books_neb']
                + counts['qty_books_prlib']
            )
            total_references_data.append(
                counts['qty_books_reference_14'] + counts['qty_books_reference_35'] +
                counts['qty_books_reference_invalid'] + counts['qty_books_reference_online']
            )

        context['dates'] = dates
        context['qty_books_14_data'] = qty_books_14_data
        context['qty_books_35_data'] = qty_books_35_data
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


class AdultBookReportCreateView(LoginRequiredMixin, CreateView):
    model = AdultBookReport
    form_class = AdultBookReportForm
    template_name = 'adult/adult_book_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('adult_books_list')


class AdultBookReportUpdateView(LoginRequiredMixin, UpdateView):
    model = AdultBookReport
    form_class = AdultBookReportForm
    template_name = 'adult/adult_book_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('adult_books_list')


class ChildVisitReportListView(LoginRequiredMixin, ListView):
    model = ChildVisitReport
    template_name = 'child/childvisits_list.html'
    context_object_name = 'visits'

    def get_queryset(self):
        user = self.request.user
        employee = Employee.objects.get(user=user)
        return ChildVisitReport.objects.filter(library=employee.branch).order_by('-date')[:15]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {"parent": "Посещения", "child": "Детская"}
        visits = self.get_queryset()

        # Подготавливаем данные для графика
        dates = []
        qty_reg_7_data = []
        qty_reg_14_data = []
        qty_reg_30_data = []
        qty_reg_other_data = []
        qty_reg_prlib_data = []
        qty_visited_14_data = []
        qty_visited_35_data = []
        qty_visited_other_data = []
        qty_visited_invalids_data = []
        qty_visited_out_station_data = []
        qty_visited_prlib_data = []
        qty_events_14_data = []
        qty_events_35_data = []
        qty_events_other_data = []
        qty_events_invalids_data = []
        qty_events_out_station_data = []
        total_reg_data = []
        total_visited_data = []
        total_events_data = []

        day_count = defaultdict(lambda: {
            'qty_reg_7': 0,
            'qty_reg_14': 0,
            'qty_reg_30': 0,
            'qty_reg_other': 0,
            'qty_reg_prlib': 0,
            'qty_visited_14': 0,
            'qty_visited_35': 0,
            'qty_visited_other': 0,
            'qty_visited_invalids': 0,
            'qty_visited_out_station': 0,
            'qty_visited_prlib': 0,
            'qty_events_14': 0,
            'qty_events_35': 0,
            'qty_events_other': 0,
            'qty_events_invalids': 0,
            'qty_events_out_station': 0,
        })

        for visit in visits:
            day_str = visit.date.strftime('%d.%m.%Y')
            day_count[day_str]['qty_reg_7'] += visit.qty_reg_7
            day_count[day_str]['qty_reg_14'] += visit.qty_reg_14
            day_count[day_str]['qty_reg_30'] += visit.qty_reg_30
            day_count[day_str]['qty_reg_other'] += visit.qty_reg_other
            day_count[day_str]['qty_reg_prlib'] += visit.qty_reg_prlib
            day_count[day_str]['qty_visited_14'] += visit.qty_visited_14
            day_count[day_str]['qty_visited_35'] += visit.qty_visited_35
            day_count[day_str]['qty_visited_other'] += visit.qty_visited_other
            day_count[day_str]['qty_visited_invalids'] += visit.qty_visited_invalids
            day_count[day_str]['qty_visited_out_station'] += visit.qty_visited_out_station
            day_count[day_str]['qty_visited_prlib'] += visit.qty_visited_prlib
            day_count[day_str]['qty_events_14'] += visit.qty_events_14
            day_count[day_str]['qty_events_35'] += visit.qty_events_35
            day_count[day_str]['qty_events_other'] += visit.qty_events_other
            day_count[day_str]['qty_events_invalids'] += visit.qty_events_invalids
            day_count[day_str]['qty_events_out_station'] += visit.qty_events_out_station

        for date, counts in sorted(day_count.items()):
            dates.append(date)
            qty_reg_7_data.append(counts['qty_reg_7'])
            qty_reg_14_data.append(counts['qty_reg_14'])
            qty_reg_30_data.append(counts['qty_reg_30'])
            qty_reg_other_data.append(counts['qty_reg_other'])
            qty_reg_prlib_data.append(counts['qty_reg_prlib'])
            qty_visited_14_data.append(counts['qty_visited_14'])
            qty_visited_35_data.append(counts['qty_visited_35'])
            qty_visited_other_data.append(counts['qty_visited_other'])
            qty_visited_invalids_data.append(counts['qty_visited_invalids'])
            qty_visited_out_station_data.append(counts['qty_visited_out_station'])
            qty_visited_prlib_data.append(counts['qty_visited_prlib'])
            qty_events_14_data.append(counts['qty_events_14'])
            qty_events_35_data.append(counts['qty_events_35'])
            qty_events_other_data.append(counts['qty_events_other'])
            qty_events_invalids_data.append(counts['qty_events_invalids'])
            qty_events_out_station_data.append(counts['qty_events_out_station'])
            total_reg_data.append(counts['qty_reg_7'] + counts['qty_reg_14'] + counts['qty_reg_30'] + counts['qty_reg_other'] + counts['qty_reg_prlib'])
            total_visited_data.append(counts['qty_visited_14'] + counts['qty_visited_35'] + counts['qty_visited_other'] + counts['qty_visited_invalids'] + counts['qty_visited_out_station'] + counts['qty_visited_prlib'])
            total_events_data.append(counts['qty_events_14'] + counts['qty_events_35'] + counts['qty_events_other'] + counts['qty_events_invalids'] + counts['qty_events_out_station'])

        context['dates'] = dates
        context['qty_reg_7_data'] = qty_reg_7_data
        context['qty_reg_14_data'] = qty_reg_14_data
        context['qty_reg_30_data'] = qty_reg_30_data
        context['qty_reg_other_data'] = qty_reg_other_data
        context['qty_reg_prlib_data'] = qty_reg_prlib_data
        context['qty_visited_14_data'] = qty_visited_14_data
        context['qty_visited_35_data'] = qty_visited_35_data
        context['qty_visited_other_data'] = qty_visited_other_data
        context['qty_visited_invalids_data'] = qty_visited_invalids_data
        context['qty_visited_out_station_data'] = qty_visited_out_station_data
        context['qty_visited_prlib_data'] = qty_visited_prlib_data
        context['qty_events_14_data'] = qty_events_14_data
        context['qty_events_35_data'] = qty_events_35_data
        context['qty_events_other_data'] = qty_events_other_data
        context['qty_events_invalids_data'] = qty_events_invalids_data
        context['qty_events_out_station_data'] = qty_events_out_station_data
        context['total_reg_data'] = total_reg_data
        context['total_visited_data'] = total_visited_data
        context['total_events_data'] = total_events_data

        return context


class ChildVisitReportCreateView(LoginRequiredMixin, CreateView):
    model = ChildVisitReport
    form_class = ChildVisitReportForm
    template_name = 'child/child_visit_form.html'
    success_url = reverse_lazy('child_visits_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('child_visits_list')


class ChildVisitReportUpdateView(LoginRequiredMixin, UpdateView):
    model = ChildVisitReport
    form_class = ChildVisitReportForm
    template_name = 'child/child_visit_form.html'
    success_url = reverse_lazy('child_visits_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('child_visits_list')


class ChildBookReportListView(LoginRequiredMixin, ListView):
    model = ChildBookReport
    template_name = 'child/childbooks_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        user = self.request.user
        employee = Employee.objects.get(user=user)
        return ChildBookReport.objects.filter(library=employee.branch).order_by('-date')[:15]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib
        context['breadcrumb'] = {"parent": "Книговыдача", "child": "Взрослая"}
        reports = self.get_queryset()

        # Подготавливаем данные для графика
        dates = []
        qty_books_14_data = []
        qty_books_30_data = []
        qty_books_other_data = []
        qty_books_neb_data = []
        qty_books_prlib_data = []
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
        qty_books_reference_30_data = []
        qty_books_reference_other_data = []
        qty_books_reference_online_data = []
        total_books_data = []
        total_references_data = []

        day_count = defaultdict(lambda: {
            'qty_books_14': 0,
            'qty_books_30': 0,
            'qty_books_other': 0,
            'qty_books_neb': 0,
            'qty_books_prlib': 0,
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
            'qty_books_reference_30': 0,
            'qty_books_reference_other': 0,
            'qty_books_reference_online': 0,
        })

        for report in reports:
            day_str = report.date.strftime('%d.%m.%Y')
            day_count[day_str]['qty_books_14'] += report.qty_books_14
            day_count[day_str]['qty_books_30'] += report.qty_books_30
            day_count[day_str]['qty_books_other'] += report.qty_books_other
            day_count[day_str]['qty_books_neb'] += report.qty_books_neb
            day_count[day_str]['qty_books_prlib'] += report.qty_books_prlib
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
            day_count[day_str]['qty_books_reference_30'] += report.qty_books_reference_30
            day_count[day_str]['qty_books_reference_other'] += report.qty_books_reference_other
            day_count[day_str]['qty_books_reference_online'] += report.qty_books_reference_online

        for date, counts in sorted(day_count.items()):
            dates.append(date)
            qty_books_14_data.append(counts['qty_books_14'])
            qty_books_30_data.append(counts['qty_books_30'])
            qty_books_other_data.append(counts['qty_books_other'])
            qty_books_neb_data.append(counts['qty_books_neb'])
            qty_books_prlib_data.append(counts['qty_books_prlib'])
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
            qty_books_reference_30_data.append(counts['qty_books_reference_30'])
            qty_books_reference_other_data.append(counts['qty_books_reference_other'])
            qty_books_reference_online_data.append(counts['qty_books_reference_online'])
            total_books_data.append(
                counts['qty_books_14'] + counts['qty_books_30'] + counts['qty_books_other'] + counts['qty_books_neb'] + counts['qty_books_prlib']
            )
            total_references_data.append(
                counts['qty_books_reference_14'] + counts['qty_books_reference_30'] + counts['qty_books_neb'] + counts['qty_books_prlib'] +
                counts['qty_books_reference_other'] + counts['qty_books_reference_online']
            )

        context['dates'] = dates
        context['qty_books_14_data'] = qty_books_14_data
        context['qty_books_30_data'] = qty_books_30_data
        context['qty_books_other_data'] = qty_books_other_data
        context['qty_books_neb_data'] = qty_books_neb_data
        context['qty_books_prlib_data'] = qty_books_prlib_data
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
        context['qty_books_reference_30_data'] = qty_books_reference_30_data
        context['qty_books_reference_other_data'] = qty_books_reference_other_data
        context['qty_books_reference_online_data'] = qty_books_reference_online_data
        context['total_books_data'] = total_books_data
        context['total_references_data'] = total_references_data

        return context


class ChildBookReportCreateView(LoginRequiredMixin, CreateView):
    model = ChildBookReport
    form_class = ChildBookReportForm
    template_name = 'child/child_book_form.html'
    success_url = reverse_lazy('child_books_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('child_books_list')


class ChildBookReportUpdateView(LoginRequiredMixin, UpdateView):
    model = ChildBookReport
    form_class = ChildBookReportForm
    template_name = 'child/child_book_form.html'
    success_url = reverse_lazy('child_books_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        branch = employee.branch
        context['mod_lib'] = branch.mod_lib
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('child_books_list')

