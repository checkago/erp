from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from .models import Event, AdultVisitReport, AdultBookReport, ChildVisitReport, ChildBookReport
from .forms import EventForm
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
    context_object_name = 'events_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        date_15_days_ago = timezone.now() - timedelta(days=15)
        context['events'] = Event.objects.filter(date__gte=date_15_days_ago, library=employee.branch).order_by('-date')
        context['breadcrumb'] = {"parent": "Дневник", "child": "Мероприятия"}
        context['form'] = EventForm(user=user)  # Создаем пустую форму для отображения с фильтрацией кафедр
        return context

    def post(self, request, *args, **kwargs):
        if 'pk' in request.POST:  # Проверяем наличие pk в POST-запросе
            pk = request.POST['pk']  # Получаем значение pk
            event_instance = get_object_or_404(Event, pk=pk)

            form = EventForm(request.POST, instance=event_instance, user=request.user)

            if form.is_valid():
                form.save()
                return redirect(
                    reverse_lazy('events_list'))  # Перенаправление на список событий после успешного обновления

            return self.get(request, *args, **kwargs)

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

    def get_event(self, pk):
        return get_object_or_404(Event, pk=pk)


class EventUpdateView(View):
    def post(self, request, *args, **kwargs):
        if 'pk' in request.POST:  # Проверяем наличие pk в POST-запросе
            pk = request.POST['pk']  # Получаем значение pk
            event_instance = get_object_or_404(Event, pk=pk)  # Получаем объект события по pk

            # Обработка состояния чекбокса "paid"
            paid_status = 'paid' in request.POST  # Проверяем наличие ключа 'paid' в POST-запросе

            form_data = request.POST.copy()
            form_data['paid'] = paid_status  # Устанавливаем состояние чекбокса

            form = EventForm(form_data, instance=event_instance)  # Создаем форму с текущими данными события
            if form.is_valid():  # Проверяем валидность формы
                form.save()  # Сохраняем изменения
                return redirect(reverse_lazy('events_list'))  # Перенаправляем на список событий после успешного обновления

        return redirect('events_list')  # Перенаправляем на список событий или обрабатываем ошибку

