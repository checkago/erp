from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from .models import Event, AdultVisitReport, AdultBookReport, ChildVisitReport, ChildBookReport
from .forms import EventForm
from ..core.models import Employee, Cafedra


class DiaryView(TemplateView):
    template_name = 'diary.html'  # Укажите путь к вашему шаблону

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['adultvisitreport'] = AdultVisitReport.objects.all()
        context['adultvisitreport'] = AdultBookReport.objects.all()
        context['childvisitreport'] = ChildVisitReport.objects.all()
        context['childvisitreport'] = ChildBookReport.objects.all()
        context['events'] = Event.objects.all()
        context['form'] = EventForm()
        return context


class EventListView(TemplateView):
    template_name = 'events/events_list.html'
    context_object_name = 'events_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_15_days_ago = timezone.now() - timedelta(days=15)
        context['events'] = Event.objects.filter(date__gte=date_15_days_ago).order_by('-date')
        context['form'] = EventForm()  # Создаем пустую форму для отображения
        return context

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        if form.is_valid():
            user = request.user
            employee = get_object_or_404(Employee, user=user)
            event_instance = form.save(commit=False)
            event_instance.library = employee.branch  # Устанавливаем библиотеку
            event_instance.save()
            return redirect(reverse_lazy('events_list'))  # Перенаправление на список событий после успешного сохранения
        else:
            # Если форма не валидна, возвращаем контекст с ошибками
            context = self.get_context_data(form=form)
            return self.render_to_response(context)


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = ''
    success_url = '/events/'  # URL to redirect after successful update

