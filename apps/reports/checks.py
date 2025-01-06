from django.db.models import Q
from django.utils import timezone
from .models import VisitReport, BookReport, Event, Branch

CHECK_DAYS = 3
BAD_LIBRARY_THRESHOLD = 5

def check_data_fillings():
    # Устанавливаем стартовую дату на 3 января текущего года
    start_date = timezone.now().replace(month=1, day=3, year=timezone.now().year).date()  # Преобразуем в date
    current_date = timezone.now().date()  # Текущая дата как date

    results = []
    branches = Branch.objects.filter(Q(adult=True) | Q(child=True) | Q(mod_lib=True))

    for branch in branches:
        # Получаем последние отчеты с учетом стартовой даты
        latest_visit_report = branch.visitreports.filter(date__gte=start_date).last()
        latest_book_report = branch.bookreports.filter(date__gte=start_date).last()
        latest_event = branch.events.filter(date__gte=start_date).last()

        # Проверяем, были ли записи внесены или исправлены после стартовой даты
        if latest_visit_report and latest_visit_report.date >= start_date:
            total_missed_days_visits = 0  # Запись была внесена или исправлена
        else:
            total_missed_days_visits = (current_date - start_date).days

        if latest_book_report and latest_book_report.date >= start_date:
            total_missed_days_books = 0  # Запись была внесена или исправлена
        else:
            total_missed_days_books = (current_date - start_date).days

        if latest_event and latest_event.date >= start_date:
            total_missed_days_events = 0  # Запись была внесена или исправлена
        else:
            total_missed_days_events = (current_date - start_date).days

        # Проверяем, есть ли пропущенные дни больше CHECK_DAYS
        if total_missed_days_visits > CHECK_DAYS or total_missed_days_books > CHECK_DAYS or total_missed_days_events > CHECK_DAYS:
            results.append({
                'branch': branch.short_name,
                'missed_days': {
                    'visits': total_missed_days_visits,
                    'books': total_missed_days_books,
                    'events': total_missed_days_events,
                },
                'date': start_date,
                'is_bad_library': (total_missed_days_visits > BAD_LIBRARY_THRESHOLD or
                                   total_missed_days_books > BAD_LIBRARY_THRESHOLD or
                                   total_missed_days_events > BAD_LIBRARY_THRESHOLD)
            })

    return results
