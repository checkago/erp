from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views
from .views import EventListView, DiaryView, EventUpdateView, EventCreateView, BookReportListView, \
    BookReportCreateView, BookReportUpdateView, VisitReportListView, VisitReportCreateView, \
    VisitReportUpdateView

urlpatterns = [
    path('diary/', DiaryView.as_view(), name='diary'),
    path('diary_svod/', views.diary_svod, name='diary-svod'),
    path('visits/', VisitReportListView.as_view(), name='visits_list'),
    path('visits/create/', VisitReportCreateView.as_view(), name='visits_create'),
    path('visits/update/<int:pk>/', VisitReportUpdateView.as_view(), name='visits_update'),
    path('books/', BookReportListView.as_view(), name='books_list'),
    path('books/create/', BookReportCreateView.as_view(), name='books_create'),
    path('books/update/<int:pk>/', BookReportUpdateView.as_view(), name='books_update'),
    path('events/', EventListView.as_view(), name='events_list'),
    path('event/create/', EventCreateView.as_view(), name='event_create'),  # Путь для создания события
    path('event/update/<int:id>/', EventUpdateView.as_view(), name='event_update'),  # Путь для обновления события

]


if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()