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


class EventListView(LoginRequiredMixin, View):
    template_name = 'events/events_list.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        employee = Employee.objects.get(user=user)
        date_15_days_ago = timezone.now() - timedelta(days=15)
        events = Event.objects.filter(date__gte=date_15_days_ago, library=employee.branch).order_by('-date')
        context = {
            'events': events,
            'breadcrumb': {"parent": "Дневник", "child": "Мероприятия"},
            'form': EventForm(user=user)
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'event_id' in request.POST:
            event_id = request.POST['event_id']
            event_instance = get_object_or_404(Event, pk=event_id)

            form = EventForm(request.POST, instance=event_instance)
            if form.is_valid():
                form.save()
                return redirect(reverse_lazy('events_list'))

        # Если форма не валидна или нет event_id
        return self.get(request, *args, **kwargs)  # Возвращаем контекст с ошибками

class EventUpdateView(UpdateView):
    model = Event
    fields = ['cafedra', 'name', 'date', 'direction', 'quantity',
              'as_part', 'age_14', 'age_35', 'age_other',
              'invalids', 'out_of_station', 'paid', 'note']
    template_name = 'events/events_list.html'
    success_url = reverse_lazy('events:events_list')

