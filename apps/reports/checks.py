from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import VisitReport, BookReport, Event, Branch

CHECK_DAYS = 3
BAD_LIBRARY_THRESHOLD = 5

def check_data_fillings():
    target_date = timezone.now() - timedelta(days=CHECK_DAYS)
    target_date_only = target_date.date()  # Преобразуем в date

    results = []
    branches = Branch.objects.filter(Q(adult=True) | Q(child=True) | Q(mod_lib=True))

    for branch in branches:
        latest_visit_report = branch.visitreports.latest('date') if branch.visitreports.exists() else None
        latest_book_report = branch.bookreports.latest('date') if branch.bookreports.exists() else None
        latest_event = branch.events.latest('date') if branch.events.exists() else None

        # Вычисляем общее количество пропущенных дней с последней записи
        total_missed_days_visits = (timezone.now().date() - latest_visit_report.date).days if latest_visit_report else 0
        total_missed_days_books = (timezone.now().date() - latest_book_report.date).days if latest_book_report else 0
        total_missed_days_events = (timezone.now().date() - latest_event.date).days if latest_event else 0

        # Проверяем, есть ли пропущенные дни больше CHECK_DAYS
        if total_missed_days_visits > CHECK_DAYS or total_missed_days_books > CHECK_DAYS or total_missed_days_events > CHECK_DAYS:
            results.append({
                'branch': branch.short_name,
                'missed_days': {
                    'visits': total_missed_days_visits,
                    'books': total_missed_days_books,
                    'events': total_missed_days_events,
                },
                'date': target_date_only,
                'is_bad_library': (total_missed_days_visits > BAD_LIBRARY_THRESHOLD or
                                   total_missed_days_books > BAD_LIBRARY_THRESHOLD or
                                   total_missed_days_events > BAD_LIBRARY_THRESHOLD)
            })

    return results
