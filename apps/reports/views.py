from django.shortcuts import get_object_or_404, redirect
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
        context['events'] = Event.objects.all()  # Получаем все события
        context['form'] = EventForm()  # Получаем пустую форму для создания Event
        return context

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        if form.is_valid():
            # Получаем библиотеку текущего пользователя
            user = request.user
            employee = get_object_or_404(Employee, user=user)
            event = form.save(commit=False)
            event.library = employee.branch  # Устанавливаем библиотеку
            event.save()
            return redirect(reverse_lazy('diary'))  # Перенаправление на ту же страницу или на другую
        return self.render_to_response({'form': form})


class EventListView(ListView):
    model = Event
    template_name = 'events/events_list.html'
    context_object_name = 'events'  # Добавлено для использования в шаблоне

class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['cafedra', 'name', 'date', 'direction', 'quantity', 'age_group', 'age_14', 'age_35', 'age_54', 'age_other', 'invalids', 'out_of_station', 'note']
    success_url = reverse_lazy('event_list')  # Проверьте имя вашего URL

    def form_valid(self, form):
        # Получаем библиотеку текущего пользователя
        user = self.request.user
        employee = get_object_or_404(Employee, user=user)
        form.instance.library = employee.branch  # Устанавливаем библиотеку
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Устанавливаем доступные кафедры в зависимости от выбранной библиотеки
        branch = self.request.user.employee.branch if hasattr(self.request.user, 'employee') else None
        if branch:
            form.fields['cafedra'].queryset = Cafedra.objects.filter(library=branch)
        return form

    def form_valid(self, form):
        # Получаем библиотеку текущего пользователя
        user = self.request.user
        employee = get_object_or_404(Employee, user=user)
        form.instance.library = employee.branch  # Устанавливаем библиотеку
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Устанавливаем доступные кафедры в зависимости от выбранной библиотеки
        branch = self.request.user.employee.branch if hasattr(self.request.user, 'employee') else None
        if branch:
            form.fields['cafedra'].queryset = Cafedra.objects.filter(library=branch)
        return form


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = ''
    success_url = '/events/'  # URL to redirect after successful update

