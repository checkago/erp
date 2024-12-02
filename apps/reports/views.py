from django.views.generic import CreateView, UpdateView, DetailView
from .models import Event
from .forms import EventForm


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = '/events/'  # URL to redirect after successful creation


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = '/events/'  # URL to redirect after successful update


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'