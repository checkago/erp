from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from .views import EventCreateView, EventUpdateView, EventDetailView


urlpatterns = [
    path('events/create/', EventCreateView.as_view(), name='event_create'),
    path('events/<pk>/update/', EventUpdateView.as_view(), name='event_update'),
    path('events/<pk>/', EventDetailView.as_view(), name='event_detail'),
]


if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()