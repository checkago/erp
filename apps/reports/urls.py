from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views
from .views import EventListView, DiaryView, EventUpdateView, EventCreateView, BookReportListView, \
    BookReportCreateView, BookReportUpdateView, VisitReportListView, VisitReportCreateView, \
    VisitReportUpdateView, export_all_reports, EventDeleteView, VisitDeleteView, BookReportDeleteView, \
    export_quarter_report, export_digital_month_report, export_nats_project_report, export_quarter_all_branches

urlpatterns = [
    path('diary/', DiaryView.as_view(), name='diary'),
    path('diary_svod/', views.diary_svod, name='diary-svod'),
    path('visits/', VisitReportListView.as_view(), name='visits_list'),
    path('visits/create/', VisitReportCreateView.as_view(), name='visits_create'),
    path('visits/update/<int:pk>/', VisitReportUpdateView.as_view(), name='visits_update'),
    path('visits/delete/<int:id>/', VisitDeleteView.as_view(), name='visits_delete'),
    path('books/', BookReportListView.as_view(), name='books_list'),
    path('books/create/', BookReportCreateView.as_view(), name='books_create'),
    path('books/update/<int:pk>/', BookReportUpdateView.as_view(), name='books_update'),
    path('books/delete/<int:id>/', BookReportDeleteView.as_view(), name='books_delete'),
    path('events/', EventListView.as_view(), name='events_list'),
    path('event/create/', EventCreateView.as_view(), name='event_create'),  # Путь для создания события
    path('event/update/<int:id>/', EventUpdateView.as_view(), name='event_update'),  # Путь для обновления события
    path('event/delete/<int:id>/', EventDeleteView.as_view(), name='event_delete'),
    path('export-all-reports/', export_all_reports, name='export_all_reports'),
    path('quarter-report/', export_quarter_report, name='export_quarter_report'),
    path('quarter-report-all/', export_quarter_all_branches, name='export_quarter_all_branches'),
    path('export_digital_month_report/', export_digital_month_report, name='export_digital_month_report'),
    path('export_nats_project_report/', export_nats_project_report, name='export_nats_project_report'),
]


if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()