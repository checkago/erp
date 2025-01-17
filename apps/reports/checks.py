from django.db.models import Q
from django.utils import timezone
from .models import VisitReport, BookReport, Event, Branch

CHECK_DAYS = 3
BAD_LIBRARY_THRESHOLD = 7

def check_data_fillings():
    # Устанавливаем текущую дату и первый день текущего года
    current_date = timezone.now().date()
    start_of_year = current_date.replace(month=1, day=1)

    results = []
    branches = Branch.objects.filter(Q(adult=True) | Q(child=True) | Q(mod_lib=True))

    for branch in branches:
        # Получаем последние отчеты только за текущий год
        latest_visit_report = branch.visitreports.filter(date__gte=start_of_year).last()
        latest_book_report = branch.bookreports.filter(date__gte=start_of_year).last()
        latest_event = branch.events.filter(date__gte=start_of_year).last()

        # Определяем даты последней записи для каждой категории
        last_visit_date = latest_visit_report.date if latest_visit_report else None
        last_book_date = latest_book_report.date if latest_book_report else None
        last_event_date = latest_event.date if latest_event else None

        # Определяем дату для проверки задержки
        check_date_visits = last_visit_date if last_visit_date else start_of_year
        check_date_books = last_book_date if last_book_date else start_of_year
        check_date_events = last_event_date if last_event_date else start_of_year

        # Вычисляем общее количество пропущенных дней с последней записи или с начала года
        total_missed_days_visits = (current_date - check_date_visits).days
        total_missed_days_books = (current_date - check_date_books).days
        total_missed_days_events = (current_date - check_date_events).days

        # Проверка на будущие даты для всех типов отчетов за текущий год, исключая уже прошедшие даты
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
