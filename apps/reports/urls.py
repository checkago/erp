from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from .views import EventListView, DiaryView, EventUpdateView, EventCreateView, AdultBookReportListView, \
    AdultBookReportCreateView, AdultBookReportUpdateView, AdultVisitReportListView, AdultVisitReportCreateView, \
    AdultVisitReportUpdateView, ChildVisitReportListView, ChildVisitReportCreateView, ChildVisitReportUpdateView, \
    ChildBookReportListView, ChildBookReportCreateView, ChildBookReportUpdateView

urlpatterns = [
    path('diary/', DiaryView.as_view(), name='diary'),
    path('visits/adult/', AdultVisitReportListView.as_view(), name='adult_visits_list'),
    path('visits/adult/create/', AdultVisitReportCreateView.as_view(), name='adult_visits_create'),
    path('visits/adult/update/<int:pk>/', AdultVisitReportUpdateView.as_view(), name='adult_visits_update'),
    path('visits/child/', ChildVisitReportListView.as_view(), name='child_visits_list'),
    path('visits/child/create/', ChildVisitReportCreateView.as_view(), name='child_visits_create'),
    path('visits/child/update/<int:pk>/', ChildVisitReportUpdateView.as_view(), name='child_visits_update'),
    path('books/adult/', AdultBookReportListView.as_view(), name='adult_books_list'),
    path('books/adult/create/', AdultBookReportCreateView.as_view(), name='adult_books_create'),
    path('books/adult/update/<int:pk>/', AdultBookReportUpdateView.as_view(), name='adult_books_update'),
    path('books/child/', ChildBookReportListView.as_view(), name='child_books_list'),
    path('books/child/create/', ChildBookReportCreateView.as_view(), name='child_books_create'),
    path('books/child/update/<int:pk>/', ChildBookReportUpdateView.as_view(), name='child_books_update'),
    path('events/', EventListView.as_view(), name='events_list'),
    path('event/create/', EventCreateView.as_view(), name='event_create'),  # Путь для создания события
    path('event/update/<int:id>/', EventUpdateView.as_view(), name='event_update'),  # Путь для обновления события

]


if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()