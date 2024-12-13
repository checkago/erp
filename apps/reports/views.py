from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from .models import Event, AdultVisitReport, AdultBookReport, ChildVisitReport, ChildBookReport
from .forms import EventForm, AdultBookReportForm, AdultVisitReportForm
from ..core.models import Employee, Cafedra


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
            day_str = event.date.strftime('%Y-%m-%d')
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


class AdultBookReportListView(LoginRequiredMixin, ListView):
    model = AdultBookReport
    template_name = 'adult/adultvisits_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        user = self.request.user
        employee = Employee.objects.get(user=user)
        return AdultBookReport.objects.filter(library=employee.branch)


class AdultBookReportCreateView(LoginRequiredMixin, CreateView):
    model = AdultBookReport
    form_class = AdultBookReportForm
    template_name = 'adult/adult_book_form.html'

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)


class AdultBookReportUpdateView(LoginRequiredMixin, UpdateView):
    model = AdultBookReport
    form_class = AdultBookReportForm
    template_name = 'adult/adult_book_form.html'

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)


class AdultVisitReportListView(LoginRequiredMixin, ListView):
    model = AdultVisitReport
    template_name = 'adult/adultvisits_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        user = self.request.user
        employee = Employee.objects.get(user=user)
        return AdultVisitReport.objects.filter(library=employee.branch)


class AdultVisitReportCreateView(LoginRequiredMixin, CreateView):
    model = AdultVisitReport
    form_class = AdultVisitReportForm
    template_name = 'adult/adult_visit_form.html'

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)


class AdultVisitReportUpdateView(LoginRequiredMixin, UpdateView):
    model = AdultVisitReport
    form_class = AdultVisitReportForm
    template_name = 'adult/adult_visit_form.html'

    def form_valid(self, form):
        form.instance.library = Employee.objects.get(user=self.request.user).branch
        return super().form_valid(form)

