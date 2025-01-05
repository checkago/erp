from django.db.models import Q
from django.utils import timezone
from .models import VisitReport, BookReport, Event, Branch

CHECK_DAYS = 2
BAD_LIBRARY_THRESHOLD = 6

def check_data_fillings():
    # Устанавливаем стартовую дату на 3 января текущего года
    start_date = timezone.now().replace(month=1, day=3, year=timezone.now().year).date()  # Преобразуем в date
    current_date = timezone.now().date()  # Текущая дата как date
    target_date_only = start_date  # Преобразуем в date

    results = []
    branches = Branch.objects.filter(Q(adult=True) | Q(child=True) | Q(mod_lib=True))

    for branch in branches:
        # Получаем последние отчеты с учетом стартовой даты
        latest_visit_report = branch.visitreports.filter(date__gte=start_date).last()
        latest_book_report = branch.bookreports.filter(date__gte=start_date).last()
        latest_event = branch.events.filter(date__gte=start_date).last()

        # Вычисляем общее количество пропущенных дней с последней записи или с начала года
        total_missed_days_visits = (current_date - latest_visit_report.date).days if latest_visit_report else (current_date - start_date).days
        total_missed_days_books = (current_date - latest_book_report.date).days if latest_book_report else (current_date - start_date).days
        total_missed_days_events = (current_date - latest_event.date).days if latest_event else (current_date - start_date).days

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
