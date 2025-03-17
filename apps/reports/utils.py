from datetime import date
from django.db.models import Sum, Count, Q, F
from apps.reports.models import VisitReport, BookReport, Event
from apps.core.models import Employee


def _aggregate_visits(queryset):
    """Вспомогательная функция для агрегации данных по посещениям."""
    return queryset.aggregate(
        total_reg=Sum('qty_reg_14') + Sum('qty_reg_15_35') + Sum('qty_reg_other') +
                  Sum('qty_reg_prlib') + Sum('qty_reg_litres') + Sum('qty_reg_out_of_station'),
        total_visited=Sum('qty_visited_14') + Sum('qty_visited_15_35') +
                      Sum('qty_visited_other') + Sum('qty_visited_online') + Sum('qty_visited_prlib') +
                      Sum('qty_visited_litres') + Sum('qty_visited_out_station')
    )


def _aggregate_books(queryset):
    return queryset.aggregate(
        total_loan=Sum('qty_books_14') + Sum('qty_books_15_35') + Sum('qty_books_other') +
                   Sum('qty_books_neb') + Sum('qty_books_prlib') + Sum('qty_books_litres') +
                   Sum('qty_books_consultant') + Sum('qty_books_local_library') +Sum('qty_books_out_of_station'),
        total_reference=Sum('qty_books_reference_do_14') + Sum('qty_books_reference_14') +
                        Sum('qty_books_reference_35')
    )


def _aggregate_events(queryset):
    """Вспомогательная функция для агрегации данных по мероприятиям."""
    return queryset.aggregate(
        total_quantity=Sum('quantity'),
        total_visitors=Sum(F('age_14') + F('age_35') + F('age_other') + F('out_of_station')),
        total_paid=Count('id', filter=Q(paid=True))
    )


def get_visits_totals(user):
    """Возвращает итоги по посещениям для текущего пользователя."""
    today = date.today()
    employee = Employee.objects.get(user=user)
    library = employee.branch

    daily_totals = _aggregate_visits(VisitReport.objects.filter(date=today, library=library))
    monthly_totals = _aggregate_visits(VisitReport.objects.filter(date__month=today.month, date__year=today.year, library=library))
    yearly_totals = _aggregate_visits(VisitReport.objects.filter(date__year=today.year, library=library))

    return {
        'daily': daily_totals,
        'monthly': monthly_totals,
        'yearly': yearly_totals,
    }


def get_book_totals(user):
    """Возвращает итоги по книговыдаче для текущего пользователя."""
    today = date.today()
    try:
        employee = Employee.objects.get(user=user)
        library = employee.branch
    except Employee.DoesNotExist:
        return {
            'daily': {'loan': {'total_loan': 0}, 'reference': {'total_reference': 0}},
            'monthly': {'loan': {'total_loan': 0}, 'reference': {'total_reference': 0}},
            'yearly': {'loan': {'total_loan': 0}, 'reference': {'total_reference': 0}},
        }

    # Агрегация данных
    daily_totals = BookReport.objects.filter(date=today, library=library).aggregate(
        total_loan=Sum('qty_books_14', default=0) + Sum('qty_books_15_35', default=0) + Sum('qty_books_other', default=0),
        total_reference=Sum('qty_books_reference_do_14', default=0) + Sum('qty_books_reference_14', default=0) + Sum('qty_books_reference_35', default=0)
                        + Sum('qty_books_reference_online', default=0)
    )

    monthly_totals = BookReport.objects.filter(date__month=today.month, date__year=today.year, library=library).aggregate(
        total_loan=Sum('qty_books_14', default=0) + Sum('qty_books_15_35', default=0) + Sum('qty_books_other', default=0),
        total_reference=Sum('qty_books_reference_do_14', default=0) + Sum('qty_books_reference_14', default=0) + Sum('qty_books_reference_35', default=0)
                        + Sum('qty_books_reference_online', default=0)
)

    yearly_totals = BookReport.objects.filter(date__year=today.year, library=library).aggregate(
        total_loan=Sum('qty_books_14', default=0) + Sum('qty_books_15_35', default=0) + Sum('qty_books_other', default=0) +
        Sum('qty_books_neb', default=0) + Sum('qty_books_prlib', default=0) + Sum('qty_books_litres', default=0) +
        Sum('qty_books_consultant', default=0) + Sum('qty_books_local_library', default=0) + Sum('qty_books_out_of_station', default=0),
        total_reference=Sum('qty_books_reference_do_14', default=0) + Sum('qty_books_reference_14', default=0) + Sum('qty_books_reference_35', default=0)
                        + Sum('qty_books_reference_online', default=0)
    )

    return {
        'daily': {
            'loan': {'total_loan': daily_totals['total_loan']},
            'reference': {'total_reference': daily_totals['total_reference']},
        },
        'monthly': {
            'loan': {'total_loan': monthly_totals['total_loan']},
            'reference': {'total_reference': monthly_totals['total_reference']},
        },
        'yearly': {
            'loan': {'total_loan': yearly_totals['total_loan']},
            'reference': {'total_reference': yearly_totals['total_reference']},
        },
    }


def get_event_totals(user):
    """Возвращает итоги по мероприятиям для текущего пользователя."""
    today = date.today()
    employee = Employee.objects.get(user=user)
    library = employee.branch

    daily_totals = _aggregate_events(Event.objects.filter(date=today, library=library))
    monthly_totals = _aggregate_events(Event.objects.filter(date__month=today.month, date__year=today.year, library=library))
    yearly_totals = _aggregate_events(Event.objects.filter(date__year=today.year, library=library))

    return {
        'daily': daily_totals,
        'monthly': monthly_totals,
        'yearly': yearly_totals,
    }


def get_notes_with_data(user):
    """Возвращает заметки с данными для текущего пользователя."""
    notes_data = []

    try:
        employee = Employee.objects.get(user=user)
        user_branch = employee.branch
    except Employee.DoesNotExist:
        user_branch = None

    if user_branch:
        # Получаем записи из модели Event
        events = Event.objects.filter(note__isnull=False, library=user_branch).exclude(note='')
        for event in events:
            notes_data.append({
                'date': event.date,
                'note': event.note,
                'model_name': 'Мероприятия',
                'edit_url': f'/reports/event/update/{event.id}/'
            })

        # Получаем записи из модели VisitReport
        visits = VisitReport.objects.filter(note__isnull=False, library=user_branch).exclude(note='')
        for visit in visits:
            notes_data.append({
                'date': visit.date,
                'note': visit.note,
                'model_name': 'Регистрация/Посещения',
                'edit_url': f'/reports/visits/update/{visit.id}/'
            })

        # Получаем записи из модели BookReport
        books = BookReport.objects.filter(note__isnull=False, library=user_branch).exclude(note='')
        for book in books:
            notes_data.append({
                'date': book.date,
                'note': book.note,
                'model_name': 'Книговыдача',
                'edit_url': f'/reports/books/update/{book.id}/'
            })

    return notes_data


def get_all_visit_totals():
    """Возвращает итоги по посещениям для всех филиалов."""
    today = date.today()

    daily_totals = _aggregate_visits(VisitReport.objects.filter(date=today))
    monthly_totals = _aggregate_visits(VisitReport.objects.filter(date__month=today.month, date__year=today.year))
    yearly_totals = _aggregate_visits(VisitReport.objects.filter(date__year=today.year))

    return {
        'daily': daily_totals,
        'monthly': monthly_totals,
        'yearly': yearly_totals,
    }


def get_all_book_totals():
    """Возвращает итоги по книговыдаче для всех филиалов."""
    today = date.today()

    daily_totals = _aggregate_books(BookReport.objects.filter(date=today))
    monthly_totals = _aggregate_books(BookReport.objects.filter(date__month=today.month, date__year=today.year))
    yearly_totals = _aggregate_books(BookReport.objects.filter(date__year=today.year))

    return {
        'daily': daily_totals,
        'monthly': monthly_totals,
        'yearly': yearly_totals,
    }


def get_all_event_totals():
    """Возвращает итоги по мероприятиям для всех филиалов."""
    today = date.today()

    daily_totals = _aggregate_events(Event.objects.filter(date=today))
    monthly_totals = _aggregate_events(Event.objects.filter(date__month=today.month, date__year=today.year))
    yearly_totals = _aggregate_events(Event.objects.filter(date__year=today.year))

    return {
        'daily': daily_totals,
        'monthly': monthly_totals,
        'yearly': yearly_totals,
    }