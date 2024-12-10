from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from .models import Event, AdultVisitReport, AdultBookReport, ChildVisitReport, ChildBookReport
from .forms import EventForm, ChildBookReportForm
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
        user = self.request.user
        employee = Employee.objects.get(user=user)

        # Получаем события за последние 15 дней
        date_15_days_ago = timezone.now() - timedelta(days=15)
        events = Event.objects.filter(date__gte=date_15_days_ago, library=employee.branch).order_by('date')

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

    def post(self, request, *args, **kwargs):
        # Обработка создания нового события
        form = EventForm(request.POST, user=request.user)

        if form.is_valid():
            event_instance = form.save(commit=False)
            event_instance.library = Employee.objects.get(user=request.user).branch  # Устанавливаем библиотеку
            event_instance.save()
            return redirect(reverse_lazy('events_list'))  # Перенаправление на список событий после успешного сохранения

        else:
            # Если форма не валидна, возвращаем контекст с ошибками
            context = self.get_context_data(form=form)
            return self.render_to_response(context)


class EventUpdateView(View):
    def post(self, request, *args, **kwargs):
        if 'pk' in request.POST:  # Проверяем наличие pk в POST-запросе
            pk = request.POST['pk']  # Получаем значение pk
            event_instance = get_object_or_404(Event, pk=pk)  # Получаем объект события по pk

            # Создаем форму с текущими данными события
            form = EventForm(request.POST, instance=event_instance)

            if form.is_valid():  # Проверяем валидность формы
                form.save()  # Сохраняем изменения
                return redirect(reverse_lazy('events_list'))  # Перенаправляем на список событий после успешного обновления

        return redirect('events_list')  # Перенаправляем на список событий или обрабатываем ошибку


class ChildBookListView(LoginRequiredMixin, TemplateView):
    template_name = 'books/childbooks_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)

        # Получаем события за последние 15 дней
        date_15_days_ago = timezone.now() - timedelta(days=15)
        reports = ChildBookReport.objects.filter(date__gte=date_15_days_ago, library=employee.branch).order_by('date')

        # Подготавливаем данные для графика (если необходимо)
        dates = []
        quantity_data = []
        qty_books_14_data = []
        age_35_data = []
        age_other_data = []
        total_age_data = []

        day_count = defaultdict(lambda: {
            'quantity': 0,
            # Добавьте остальные поля по необходимости
        })

        for report in reports:
            day_str = report.date.strftime('%Y-%m-%d')
            day_count[day_str]['quantity'] += report.qty_books_14  # Пример использования поля

        for date, counts in sorted(day_count.items()):
            dates.append(date)
            quantity_data.append(counts['quantity'])
            # Заполните остальные данные по необходимости

        context['reports'] = reports  # Измените на reports
        context['dates'] = dates
        context['quantity_data'] = quantity_data
        # Добавьте остальные данные по необходимости

        context['form'] = ChildBookReportForm(user=user)  # Используйте новую форму

        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('pk'):  # Проверяем наличие pk в POST-запросе для редактирования
            pk = request.POST['pk']
            report_instance = get_object_or_404(ChildBookReport, pk=pk)

            form = ChildBookReportForm(request.POST, instance=report_instance)  # Создаем форму с текущими данными события

            if form.is_valid():
                form.save()
                return redirect(reverse_lazy('events_list'))  # Перенаправление на список событий после успешного обновления

            else:
                context = self.get_context_data(form=form)
                return self.render_to_response(context)

        else:  # Обработка создания нового события
            form = ChildBookReportForm(request.POST)

            if form.is_valid():
                report_instance = form.save(commit=False)
                report_instance.library = Employee.objects.get(user=request.user).branch  # Устанавливаем библиотеку
                report_instance.save()
                return redirect(reverse_lazy('events_list'))  # Перенаправление на список событий после успешного сохранения

            else:
                context = self.get_context_data(form=form)
                return self.render_to_response(context)

