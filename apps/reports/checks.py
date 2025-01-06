from django.db.models import Q
from django.utils import timezone
from .models import VisitReport, BookReport, Event, Branch

CHECK_DAYS = 3
BAD_LIBRARY_THRESHOLD = 7

def check_data_fillings():
    # Устанавливаем стартовую дату на 3 января текущего года
    start_date = timezone.now().replace(month=1, day=3, year=timezone.now().year).date()
    current_date = timezone.now().date()

    results = []
    branches = Branch.objects.filter(Q(adult=True) | Q(child=True) | Q(mod_lib=True))

    for branch in branches:
        # Получаем последние отчеты
        latest_visit_report = branch.visitreports.last()
        latest_book_report = branch.bookreports.last()
        latest_event = branch.events.last()

        # Определяем даты последней записи для каждой категории
        last_visit_date = latest_visit_report.date if latest_visit_report else None
        last_book_date = latest_book_report.date if latest_book_report else None
        last_event_date = latest_event.date if latest_event else None

        # Определяем дату для проверки задержки
        check_date_visits = last_visit_date if last_visit_date and last_visit_date >= start_date else start_date
        check_date_books = last_book_date if last_book_date and last_book_date >= start_date else start_date
        check_date_events = last_event_date if last_event_date and last_event_date >= start_date else start_date

        # Вычисляем общее количество пропущенных дней с последней записи или с начала года
        total_missed_days_visits = (current_date - check_date_visits).days
        total_missed_days_books = (current_date - check_date_books).days
        total_missed_days_events = (current_date - check_date_events).days

        # Проверка на будущие даты для всех типов отчетов
        future_visits = VisitReport.objects.filter(library=branch, date__gt=current_date)
        future_books = BookReport.objects.filter(library=branch, date__gt=current_date)
        future_events = Event.objects.filter(library=branch, date__gt=current_date)

        # Добавляем результаты в список только если есть пропущенные дни или будущие записи
        if (total_missed_days_visits >= CHECK_DAYS or
            total_missed_days_books >= CHECK_DAYS or
            total_missed_days_events >= CHECK_DAYS or
            future_visits.exists() or
            future_books.exists() or
            future_events.exists()):
            results.append({
                'branch': branch.short_name,
                'missed_days': {
                    'visits': total_missed_days_visits,
                    'books': total_missed_days_books,
                    'events': total_missed_days_events,
                },
                'date': max(
                    (last_visit_date if total_missed_days_visits >= CHECK_DAYS else None,
                     last_book_date if total_missed_days_books >= CHECK_DAYS else None,
                     last_event_date if total_missed_days_events >= CHECK_DAYS else None),
                    key=lambda d: d if d is not None else timezone.datetime.min.date()
                ),
                'has_future_records': future_visits.exists() or future_books.exists() or future_events.exists(),  # Флаг для будущих записей
                'future_records': {
                    'visits': future_visits,
                    'books': future_books,
                    'events': future_events,
                }
            })

    return results
