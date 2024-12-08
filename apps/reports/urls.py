from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from .views import EventListView, DiaryView, EventUpdateView

urlpatterns = [
    path('diary/', DiaryView.as_view(), name='diary'),
    path('visits/', EventListView.as_view(), name='visits_list'),
    path('visits/update/<int:pk>/', EventUpdateView.as_view(), name='update_visits'),
    path('books/', EventListView.as_view(), name='books_list'),
    path('books/update/<int:pk>/', EventUpdateView.as_view(), name='update_books'),
    path('events/', EventListView.as_view(), name='events_list'),
    path('events/update/<int:pk>/', EventUpdateView.as_view(), name='update_event'),
]


if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()