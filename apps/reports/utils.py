from datetime import date
from django.db.models import Sum, Count, Q, F
from apps.reports.models import VisitReport, BookReport, Event
from apps.core.models import Employee


def get_visits_totals(user):
    today = date.today()

    # Получаем библиотеку, к которой принадлежит пользователь
    employee = Employee.objects.get(user=user)
    library = employee.branch

    # Итоги за текущий день
    daily_totals = VisitReport.objects.filter(date=today, library=library).aggregate(
        total_reg=Sum('qty_reg_14') + Sum('qty_reg_15_35') +
                  Sum('qty_reg_other') + Sum('qty_reg_invalid') +
                  Sum('qty_reg_prlib') + Sum('qty_reg_litres'),
        total_visited=Sum('qty_visited_14') + Sum('qty_visited_15_35') +
                      Sum('qty_visited_other') + Sum('qty_visited_invalids') +
                      Sum('qty_visited_out_station') +
                      Sum('qty_visited_online') +
                      Sum('qty_visited_prlib') + Sum('qty_visited_litres')
    )

    # Итоги за текущий месяц
    monthly_totals = VisitReport.objects.filter(date__month=today.month, date__year=today.year,
                                                library=library).aggregate(
        total_reg=Sum('qty_reg_14') + Sum('qty_reg_15_35') +
                  Sum('qty_reg_other') + Sum('qty_reg_invalid') +
                  Sum('qty_reg_prlib') + Sum('qty_reg_litres'),
        total_visited=Sum('qty_visited_14') + Sum('qty_visited_15_35') +
                      Sum('qty_visited_other') + Sum('qty_visited_invalids') +
                      Sum('qty_visited_out_station') +
                      Sum('qty_visited_online') +
                      Sum('qty_visited_prlib') + Sum('qty_visited_litres')
    )

    # Итоги за текущий год
    yearly_totals = VisitReport.objects.filter(date__year=today.year, library=library).aggregate(
        total_reg=Sum('qty_reg_14') + Sum('qty_reg_15_35') +
                  Sum('qty_reg_other') + Sum('qty_reg_invalid') +
                  Sum('qty_reg_prlib') + Sum('qty_reg_litres'),
        total_visited=Sum('qty_visited_14') + Sum('qty_visited_15_35') +
                      Sum('qty_visited_other') + Sum('qty_visited_invalids') +
                      Sum('qty_visited_out_station') +
                      Sum('qty_visited_online') +
                      Sum('qty_visited_prlib') + Sum('qty_visited_litres')
    )

    return {
        'daily': daily_totals,
        'monthly': monthly_totals,
        'yearly': yearly_totals,
    }


def get_book_totals(user):
    today = date.today()

    # Получаем библиотеку, к которой принадлежит пользователь
    employee = Employee.objects.get(user=user)
    library = employee.branch

    # Итоги по книговыдаче
    daily_totals_loan = BookReport.objects.filter(date=today, library=library).aggregate(
        total_loan=Sum('qty_books_14') + Sum('qty_books_15_35') + Sum('qty_books_other') +
                   Sum('qty_books_invalid') + Sum('qty_books_neb') +
                   Sum('qty_books_prlib') + Sum('qty_books_litres') +
                   Sum('qty_books_consultant') + Sum('qty_books_local_library')
    )

    monthly_totals_loan = BookReport.objects.filter(date__month=today.month, date__year=today.year,
                                                    library=library).aggregate(
        total_loan=Sum('qty_books_14') + Sum('qty_books_15_35') + Sum('qty_books_other') +
                   Sum('qty_books_invalid') + Sum('qty_books_neb') +
                   Sum('qty_books_prlib') + Sum('qty_books_litres') +
                   Sum('qty_books_consultant') + Sum('qty_books_local_library')
    )

    yearly_totals_loan = BookReport.objects.filter(date__year=today.year, library=library).aggregate(
        total_loan=Sum('qty_books_14') + Sum('qty_books_15_35') + Sum('qty_books_other') +
                   Sum('qty_books_invalid') + Sum('qty_books_neb') +
                   Sum('qty_books_prlib') + Sum('qty_books_litres') +
                   Sum('qty_books_consultant') + Sum('qty_books_local_library')
    )

    # Итоги по справкам
    daily_totals_reference = BookReport.objects.filter(date=today, library=library).aggregate(
        total_reference=Sum('qty_books_reference_do_14') + Sum('qty_books_reference_14') +
                        Sum('qty_books_reference_35') + Sum('qty_books_reference_other') +
                        Sum('qty_books_reference_invalid') +
                        Sum('qty_books_reference_online')
    )

    monthly_totals_reference = BookReport.objects.filter(date__month=today.month, date__year=today.year,
                                                         library=library).aggregate(
        total_reference=Sum('qty_books_reference_do_14') + Sum('qty_books_reference_14') +
                        Sum('qty_books_reference_35') + Sum('qty_books_reference_other') +
                        Sum('qty_books_reference_invalid') +
                        Sum('qty_books_reference_online')
    )

    yearly_totals_reference = BookReport.objects.filter(date__year=today.year, library=library).aggregate(
        total_reference=Sum('qty_books_reference_do_14') + Sum('qty_books_reference_14') +
                        Sum('qty_books_reference_35') + Sum('qty_books_reference_other') +
                        Sum('qty_books_reference_invalid') +
                        Sum('qty_books_reference_online')
    )

    return {
        'daily': {
            'loan': daily_totals_loan,
            'reference': daily_totals_reference,
        },
        'monthly': {
            'loan': monthly_totals_loan,
            'reference': monthly_totals_reference,
        },
        'yearly': {
            'loan': yearly_totals_loan,
            'reference': yearly_totals_reference,
        },
    }


def get_event_totals(user):
    today = date.today()

    # Получаем библиотеку, к которой принадлежит пользователь
    employee = Employee.objects.get(user=user)
    library = employee.branch

    # Итоги по количеству мероприятий и посетителей
    daily_totals_events = Event.objects.filter(date=today, library=library).aggregate(
        total_quantity=Sum('quantity'),  # Общее количество мероприятий
        total_visitors=Sum(
            F('age_14') + F('age_35') + F('age_other') +
            F('invalids') + F('out_of_station') +
            F('online')
        ),
        total_paid=Count('id', filter=Q(paid=True))  # Количество платных мероприятий
    )

    # Итоги за текущий месяц
    monthly_totals_events = Event.objects.filter(date__month=today.month, date__year=today.year,
                                                 library=library).aggregate(
        total_quantity=Sum('quantity'),  # Общее количество мероприятий
        total_visitors=Sum(
            F('age_14') + F('age_35') + F('age_other') +
            F('invalids') + F('out_of_station') +
            F('online')
        ),
        total_paid=Count('id', filter=Q(paid=True))  # Количество платных мероприятий
    )

    # Итоги за текущий год
    yearly_totals_events = Event.objects.filter(date__year=today.year, library=library).aggregate(
        total_quantity=Sum('quantity'),  # Общее количество мероприятий
        total_visitors=Sum(
            F('age_14') + F('age_35') + F('age_other') +
            F('invalids') + F('out_of_station') +
            F('online')
        ),
        total_paid=Count('id', filter=Q(paid=True))  # Количество платных мероприятий
    )

    return {
        'daily': daily_totals_events,
        'monthly': monthly_totals_events,
        'yearly': yearly_totals_events,
    }


def get_notes_with_data():
    notes_data = []

    # Получаем записи из модели Event
    events = Event.objects.filter(note__isnull=False).exclude(note='')
    for event in events:
        notes_data.append({
            'date': event.date,
            'note': event.note,
            'model_name': 'Мероприятия',
            'edit_url': f'/reports/event/update/{event.id}/'  # URL для редактирования события
        })

    # Получаем записи из модели VisitReport
    visits = VisitReport.objects.filter(note__isnull=False).exclude(note='')
    for visit in visits:
        notes_data.append({
            'date': visit.date,
            'note': visit.note,
            'model_name': 'Регистрация/Посещения',
            'edit_url': f'/reports/visits/update/{visit.id}/'  # URL для редактирования отчета посещений
        })

    # Получаем записи из модели BookReport
    books = BookReport.objects.filter(note__isnull=False).exclude(note='')
    for book in books:
        notes_data.append({
            'date': book.date,
            'note': book.note,
            'model_name': 'Книговыдача',
            'edit_url': f'/reports/books/update/{book.id}/'  # URL для редактирования отчета книговыдачи
        })

    return notes_data


def get_all_totals():
    today = date.today()
    # Итоги за текущий день
    daily_totals = VisitReport.objects.filter(date=today).aggregate(
        total_reg=Sum('qty_reg_14') + Sum('qty_reg_15_35') + Sum('qty_reg_other') + Sum(
            'qty_reg_invalid') + Sum('qty_reg_prlib') + Sum('qty_reg_litres'),
        total_visited=Sum('qty_visited_14') + Sum('qty_visited_15_35') + Sum('qty_visited_other') + Sum(
            'qty_visited_invalids') + Sum('qty_visited_out_station') + Sum('qty_visited_online') + Sum(
            'qty_visited_prlib') + Sum('qty_visited_litres')
    )
    # Итоги за текущий месяц
    monthly_totals = VisitReport.objects.filter(date__month=today.month, date__year=today.year).aggregate(
        total_reg=Sum('qty_reg_14') + Sum('qty_reg_15_35') + Sum('qty_reg_other') + Sum(
            'qty_reg_invalid') + Sum('qty_reg_prlib') + Sum('qty_reg_litres'),
        total_visited=Sum('qty_visited_14') + Sum('qty_visited_15_35') + Sum('qty_visited_other') + Sum(
            'qty_visited_invalids') + Sum('qty_visited_out_station') + Sum('qty_visited_online') + Sum(
            'qty_visited_prlib') + Sum('qty_visited_litres')
    )
    # Итоги за текущий год
    yearly_totals = VisitReport.objects.filter(date__year=today.year).aggregate(
        total_reg=Sum('qty_reg_14') + Sum('qty_reg_15_35') + Sum('qty_reg_other') + Sum(
            'qty_reg_invalid') + Sum('qty_reg_prlib') + Sum('qty_reg_litres'),
        total_visited=Sum('qty_visited_14') + Sum('qty_visited_15_35') + Sum('qty_visited_other') + Sum(
            'qty_visited_invalids') + Sum('qty_visited_out_station') + Sum('qty_visited_online') + Sum(
            'qty_visited_prlib') + Sum('qty_visited_litres')
    )
    return {'daily': daily_totals, 'monthly': monthly_totals, 'yearly': yearly_totals}


def get_all_book_totals():
    today = date.today()
    # Итоги по книговыдаче
    daily_totals_loan = BookReport.objects.filter(date=today).aggregate(
        total_loan=Sum('qty_books_14') + Sum('qty_books_15_35') + Sum('qty_books_other') + Sum(
            'qty_books_invalid') + Sum('qty_books_neb') + Sum('qty_books_prlib') + Sum('qty_books_litres') + Sum(
            'qty_books_consultant') + Sum('qty_books_local_library')
    )
    monthly_totals_loan = BookReport.objects.filter(date__month=today.month, date__year=today.year).aggregate(
        total_loan=Sum('qty_books_14') + Sum(' qty_books_15_35 ') + ...
    )
    yearly_totals_loan = BookReport.objects.filter(date__year=today.year).aggregate(
        total_loan=Sum(...)
    )
    # Итоги по справкам
    daily_totals_reference = BookReport.objects.filter(date=today).aggregate(
        total_reference=Sum(...)
    )
    monthly_totals_reference = BookReport.objects.filter(date__month=today.month, date__year=today.year).aggregate(
        total_reference=Sum(...)
    )
    yearly_totals_reference = BookReport.objects.filter(date__year=today.year).aggregate(
        total_reference=Sum(...)
    )
    return {'daily': {'loan': daily_totals_loan, 'reference': daily_totals_reference},
            'monthly': {'loan': monthly_totals_loan, 'reference': monthly_totals_reference},
            'yearly': {'loan': yearly_totals_loan, 'reference': yearly_totals_reference}}


def get_all_event_totals():
    today = date.today()
    # Итоги по количеству мероприятий и посетителей
    daily_totals_events = Event.objects.filter(date=today).aggregate(
        total_quantity=Sum(...),
        total_visitors=Sum(...),
        total_paid=Count(...)
    )
    monthly_totals_events = Event.objects.filter(date__month=today.month, date__year=today.year).aggregate(
        total_quantity=Sum(...),
        total_visitors=Sum(...),
        total_paid=Count(...)
    )
    yearly_totals_events = Event.objects.filter(date__year=today.year).aggregate(
        total_quantity=Sum(...),
        total_visitors=Sum(...),
        total_paid=Count(...)
    )
    return {'daily': daily_totals_events, 'monthly': monthly_totals_events, 'yearly': yearly_totals_events}


def get_all_notes_with_data(user):
    notes_data = []

    # Получаем запись сотрудника для текущего пользователя
    try:
        employee = Employee.objects.get(user=user)
        user_branch = employee.branch  # Получаем филиал
    except Employee.DoesNotExist:
        user_branch = None  # Если сотрудник не найден

    # Получаем записи из модели Event
    events = Event.objects.filter(note__isnull=False, library=user_branch).exclude(note='').all()
    for event in events:
        notes_data.append({
            'date': event.date,
            'note': event.note,
            'model_name': 'Мероприятия',
            'edit_url': f'/reports/event/update/{event.id}/'
        })

    # Получаем записи из модели VisitReport
    visits = VisitReport.objects.filter(note__isnull=False, library=user_branch).exclude(note='').all()
    for visit in visits:
        notes_data.append({
            'date': visit.date,
            'note': visit.note,
            'model_name': 'Регистрация/Посещения',
            'edit_url': f'/reports/visits/update/{visit.id}/'
        })

    # Получаем записи из модели BookReport
    books = BookReport.objects.filter(note__isnull=False, library=user_branch).exclude(note='').all()
    for book in books:
        notes_data.append({
            'date': book.date,
            'note': book.note,
            'model_name': 'Книговыдача',
            'edit_url': f'/reports/books/update/{book.id}/'
        })

    return notes_data


def get_totals(user):
    today = date.today()

    # Получаем библиотеку, к которой принадлежит пользователь
    employee = Employee.objects.get(user=user)
    library = employee.branch

    # Итоги за текущий день
    daily_totals = VisitReport.objects.filter(date=today, library=library).aggregate(
        total_reg=Sum('qty_reg_14') + Sum('qty_reg_15_35') +
                  Sum('qty_reg_other') + Sum('qty_reg_invalid') +
                  Sum('qty_reg_prlib') + Sum('qty_reg_litres'),
        total_visited=Sum('qty_visited_14') + Sum('qty_visited_15_35') +
                      Sum('qty_visited_other') + Sum('qty_visited_invalids') +
                      Sum('qty_visited_out_station') +
                      Sum('qty_visited_online') +
                      Sum('qty_visited_prlib') + Sum('qty_visited_litres')
    )

    return {
        'daily': daily_totals,
    }


def get_all_visit_totals():
    today = date.today()

    # Итоги за текущий день
    daily_totals = VisitReport.objects.filter(date=today).aggregate(
        total_reg=Sum('qty_reg_14') + Sum('qty_reg_15_35') +
                  Sum('qty_reg_other') + Sum('qty_reg_invalid') +
                  Sum('qty_reg_prlib') + Sum('qty_reg_litres'),
        total_visited=Sum('qty_visited_14') + Sum('qty_visited_15_35') +
                      Sum('qty_visited_other') + Sum('qty_visited_invalids') +
                      Sum('qty_visited_out_station') +
                      Sum('qty_visited_online') +
                      Sum('qty_visited_prlib') + Sum('qty_visited_litres')
    )

    # Итоги за текущий месяц
    monthly_totals = VisitReport.objects.filter(date__month=today.month, date__year=today.year).aggregate(
        total_reg=Sum('qty_reg_14') + Sum('qty_reg_15_35') +
                  Sum('qty_reg_other') + Sum('qty_reg_invalid') +
                  Sum('qty_reg_prlib') + Sum('qty_reg_litres'),
        total_visited=Sum('qty_visited_14') + Sum('qty_visited_15_35') +
                      Sum('qty_visited_other') + Sum('qty_visited_invalids') +
                      Sum('qty_visited_out_station') +
                      Sum('qty_visited_online') +
                      Sum('qty_visited_prlib') + Sum('qty_visited_litres')
    )

    # Итоги за текущий год
    yearly_totals = VisitReport.objects.filter(date__year=today.year).aggregate(
        total_reg=Sum('qty_reg_14') + Sum('qty_reg_15_35') +
                  Sum('qty_reg_other') + Sum('qty_reg_invalid') +
                  Sum('qty_reg_prlib') + Sum('qty_reg_litres'),
        total_visited=Sum('qty_visited_14') + Sum('qty_visited_15_35') +
                      Sum('qty_visited_other') + Sum('qty_visited_invalids') +
                      Sum('qty_visited_out_station') +
                      Sum('qty_visited_online') +
                      Sum('qty_visited_prlib') + Sum('qty_visited_litres')
    )

    return {
        'daily': daily_totals,
        'monthly': monthly_totals,
        'yearly': yearly_totals,
    }

def get_all_book_totals():
    today = date.today()

    # Итоги по книговыдаче за текущий день
    daily_totals_loan = BookReport.objects.filter(date=today).aggregate(
        total_loan=Sum('qty_books_14') + Sum('qty_books_15_35') + Sum('qty_books_other') +
                   Sum('qty_books_invalid') + Sum('qty_books_neb') +
                   Sum('qty_books_prlib') + Sum('qty_books_litres') +
                   Sum('qty_books_consultant') + Sum('qty_books_local_library')
    )

    # Итоги за текущий месяц
    monthly_totals_loan = BookReport.objects.filter(date__month=today.month, date__year=today.year).aggregate(
        total_loan=Sum('qty_books_14') + Sum('qty_books_15_35') + Sum('qty_books_other') +
                   Sum('qty_books_invalid') + Sum('qty_books_neb') +
                   Sum('qty_books_prlib') + Sum('qty_books_litres') +
                   Sum('qty_books_consultant') + Sum('qty_books_local_library')
    )

    # Итоги за текущий год
    yearly_totals_loan = BookReport.objects.filter(date__year=today.year).aggregate(
        total_loan=Sum('qty_books_14') + Sum('qty_books_15_35') + Sum('qty_books_other') +
                   Sum('qty_books_invalid') + Sum('qty_books_neb') +
                   Sum('qty_books_prlib') + Sum('qty_books_litres') +
                   Sum('qty_books_consultant') + Sum('qty_books_local_library')
    )

    # Итоги по справкам за текущий день
    daily_totals_reference = BookReport.objects.filter(date=today).aggregate(
        total_reference=Sum('qty_books_reference_do_14') + Sum('qty_books_reference_14') +
                        Sum('qty_books_reference_35') + Sum('qty_books_reference_other') +
                        Sum('qty_books_reference_invalid') +
                        Sum('qty_books_reference_online')
    )

    # Итоги по справкам за текущий месяц
    monthly_totals_reference = BookReport.objects.filter(date__month=today.month, date__year=today.year).aggregate(
        total_reference=Sum('qty_books_reference_do_14') + Sum('qty_books_reference_14') +
                        Sum('qty_books_reference_35') + Sum('qty_books_reference_other') +
                        Sum('qty_books_reference_invalid') +
                        Sum('qty_books_reference_online')
    )

    # Итоги по справкам за текущий год
    yearly_totals_reference = BookReport.objects.filter(date__year=today.year).aggregate(
        total_reference=Sum('qty_books_reference_do_14') + Sum('qty_books_reference_14') +
                        Sum('qty_books_reference_35') + Sum('qty_books_reference_other') +
                        Sum('qty_books_reference_invalid') +
                        Sum('qty_books_reference_online')
    )

    return {
        'daily': {
            'loan': daily_totals_loan,
            'reference': daily_totals_reference,
        },
        'monthly': {
            'loan': monthly_totals_loan,
            'reference': monthly_totals_reference,
        },
        'yearly': {
            'loan': yearly_totals_loan,
            'reference': yearly_totals_reference,
        },
    }

def get_all_event_totals():
    today = date.today()

    # Итоги по количеству мероприятий и посетителей за текущий день
    daily_totals_events = Event.objects.filter(date=today).aggregate(
        total_quantity=Sum("quantity"),
        total_visitors=Sum(
            F("age_14") + F("age_35") + F("age_other") +
            F("invalids") + F("out_of_station") +
            F("online")
        ),
        total_paid=Count("id", filter=Q(paid=True))
    )

    # Итоги за текущий месяц
    monthly_totals_events = Event.objects.filter(date__month=today.month, date__year=today.year).aggregate(
        total_quantity=Sum("quantity"),
        total_visitors=Sum(
            F("age_14") + F("age_35") + F("age_other") +
            F("invalids") + F("out_of_station") +
            F("online")
        ),
        total_paid=Count("id", filter=Q(paid=True))
    )

    # Итоги за текущий год
    yearly_totals_events = Event.objects.filter(date__year=today.year).aggregate(
        total_quantity=Sum("quantity"),
        total_visitors=Sum(
            F("age_14") + F("age_35") + F("age_other") +
            F("invalids") + F("out_of_station") +
            F("online")
        ),
        total_paid=Count("id", filter=Q(paid=True))
    )

    return {
        "daily": daily_totals_events,
        "monthly": monthly_totals_events,
        "yearly": yearly_totals_events,
    }

