import os
import calendar
from urllib.parse import quote

import openpyxl
from django.db import models
from django.http import HttpResponse
from django.utils.formats import date_format

from .models import VisitReport, BookReport, Event, VisitsFirstData, EventsFirstData, VisitPlan, EventsPlan
from apps.core.models import Employee, Branch
from datetime import datetime, date


def generate_all_reports_excel(user, year, month):
    # Получаем сотрудника и филиал
    try:
        employee = Employee.objects.get(user=user)
        branch = employee.branch
    except Employee.DoesNotExist:
        return None

    if not branch:
        return None

    # Загружаем общий шаблон
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, 'reports/excell/report_all_template.xlsx')

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"File not found: {template_path}")

    wb = openpyxl.load_workbook(filename=template_path)

    # Генерация отчёта по посещениям
    generate_visit_report(wb, branch, year, month)

    # Генерация отчёта по книговыдаче
    generate_book_report(wb, branch, year, month)

    # Генерация отчёта по мероприятиям
    generate_events_report(wb, branch, year, month)

    # Сохраняем файл в HttpResponse
    month_name = calendar.month_name[month]
    filename = f"all_reports_{branch.short_name}_{year}_{month_name}.xlsx"
    safe_filename = quote(filename)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
    wb.save(response)
    return response

def generate_visit_report(wb, branch, year, month):
    ws = wb["Число пользователей+посещения"]

    # Фильтруем отчеты по филиалу, году и месяцу
    visit_reports = VisitReport.objects.filter(
        library=branch,
        date__year=year,
        date__month=month
    ).order_by('date')

    # Фильтруем отчеты с начала года до текущего месяца (не включая текущий месяц)
    visit_reports_year = VisitReport.objects.filter(
        library=branch,
        date__year=year,
        date__month__lt=month
    ).order_by('date')

    # Агрегируем данные с начала года
    year_start_data = {
        'qty_reg_14': sum(report.qty_reg_14 for report in visit_reports_year),
        'qty_reg_15_35': sum(report.qty_reg_15_35 for report in visit_reports_year),
        'qty_reg_other': sum(report.qty_reg_other for report in visit_reports_year),
        'qty_reg_pensioners': sum(report.qty_reg_pensioners for report in visit_reports_year),
        'qty_reg_invalid': sum(report.qty_reg_invalid for report in visit_reports_year),
        'qty_visited_14': sum(report.qty_visited_14 for report in visit_reports_year),
        'qty_visited_15_35': sum(report.qty_visited_15_35 for report in visit_reports_year),
        'qty_visited_other': sum(report.qty_visited_other for report in visit_reports_year),
        'qty_visited_pensioners': sum(report.qty_visited_pensioners for report in visit_reports_year),
        'qty_visited_invalids': sum(report.qty_visited_invalids for report in visit_reports_year),
        'qty_visited_out_station': sum(report.qty_visited_out_station for report in visit_reports_year),
        'qty_visited_online': sum(report.qty_visited_online for report in visit_reports_year),
    }

    # Записываем данные с начала года в строку 6
    ws['B6'] = year_start_data['qty_reg_14'] + year_start_data['qty_reg_15_35'] + year_start_data['qty_reg_other']
    ws['C6'] = year_start_data['qty_reg_14']
    ws['D6'] = year_start_data['qty_reg_15_35']
    ws['E6'] = year_start_data['qty_reg_other']
    ws['F6'] = year_start_data['qty_reg_pensioners']
    ws['G6'] = year_start_data['qty_reg_invalid']
    ws['H6'] = year_start_data['qty_visited_14'] + year_start_data['qty_visited_15_35'] + year_start_data['qty_visited_other']
    ws['I6'] = year_start_data['qty_visited_14']
    ws['J6'] = year_start_data['qty_visited_15_35']
    ws['K6'] = year_start_data['qty_visited_other']
    ws['L6'] = year_start_data['qty_visited_pensioners']
    ws['M6'] = year_start_data['qty_visited_invalids']
    ws['N6'] = year_start_data['qty_visited_out_station']
    ws['O6'] = year_start_data['qty_visited_online']

    # Заполняем данные за текущий месяц
    current_date = date(year, month, 1)
    month_name_ru = date_format(current_date, "F")
    ws['A1'] = f"Отчет по посещениям за {month_name_ru} {year} года"
    ws['L1'] = f"{branch}"

    row_num = 7  # Начинаем с 7 строки (после заголовков)
    for report in visit_reports:
        # Вставляем строку перед записью данных (кроме первой строки)
        if row_num > 7:
            ws.insert_rows(row_num)  # Вставляем новую строку
            for col in range(1, ws.max_column + 1):
                ws.cell(row=row_num, column=col)._style = ws.cell(row=7, column=col)._style  # Копируем стили

        # Записываем данные в текущую строку
        ws[f'A{row_num}'] = report.date.strftime('%d.%m.%Y')
        ws[f'B{row_num}'] = report.qty_reg_14 + report.qty_reg_15_35 + report.qty_reg_other
        ws[f'C{row_num}'] = report.qty_reg_14
        ws[f'D{row_num}'] = report.qty_reg_15_35
        ws[f'E{row_num}'] = report.qty_reg_other
        ws[f'F{row_num}'] = report.qty_reg_pensioners
        ws[f'G{row_num}'] = report.qty_reg_invalid
        ws[f'H{row_num}'] = report.qty_visited_14 + report.qty_visited_15_35 + report.qty_visited_other
        ws[f'I{row_num}'] = report.qty_visited_14
        ws[f'J{row_num}'] = report.qty_visited_15_35
        ws[f'K{row_num}'] = report.qty_visited_other
        ws[f'L{row_num}'] = report.qty_visited_pensioners
        ws[f'M{row_num}'] = report.qty_visited_invalids
        ws[f'N{row_num}'] = report.qty_visited_out_station
        ws[f'O{row_num}'] = report.qty_visited_online
        ws[f'P{row_num}'] = report.note
        row_num += 1


def generate_book_report(wb, branch, year, month):
    ws = wb["Книговыдача"]

    # Фильтруем отчеты по филиалу, году и месяцу
    book_reports = BookReport.objects.filter(
        library=branch,
        date__year=year,
        date__month=month
    ).order_by('date')

    # Фильтруем отчеты с начала года до текущего месяца (не включая текущий месяц)
    book_reports_year = BookReport.objects.filter(
        library=branch,
        date__year=year,
        date__month__lt=month
    ).order_by('date')

    # Агрегируем данные с начала года
    year_start_data = {
        'qty_books_14': sum(report.qty_books_14 for report in book_reports_year),
        'qty_books_15_35': sum(report.qty_books_15_35 for report in book_reports_year),
        'qty_books_other': sum(report.qty_books_other for report in book_reports_year),
        'qty_books_invalid': sum(report.qty_books_invalid for report in book_reports_year),
        'qty_books_neb': sum(report.qty_books_neb for report in book_reports_year),
        'qty_books_prlib': sum(report.qty_books_prlib for report in book_reports_year),
        'qty_books_litres': sum(report.qty_books_litres for report in book_reports_year),
        'qty_books_consultant': sum(report.qty_books_consultant for report in book_reports_year),
        'qty_books_local_library': sum(report.qty_books_local_library for report in book_reports_year),
        'qty_books_part_opl': sum(report.qty_books_part_opl for report in book_reports_year),
        'qty_books_part_enm': sum(report.qty_books_part_enm for report in book_reports_year),
        'qty_books_part_tech': sum(report.qty_books_part_tech for report in book_reports_year),
        'qty_books_part_sh': sum(report.qty_books_part_sh for report in book_reports_year),
        'qty_books_part_si': sum(report.qty_books_part_si for report in book_reports_year),
        'qty_books_part_yl': sum(report.qty_books_part_yl for report in book_reports_year),
        'qty_books_part_hl': sum(report.qty_books_part_hl for report in book_reports_year),
        'qty_books_part_dl': sum(report.qty_books_part_dl for report in book_reports_year),
        'qty_books_part_other': sum(report.qty_books_part_other for report in book_reports_year),
        'qty_books_part_audio': sum(report.qty_books_part_audio for report in book_reports_year),
        'qty_books_part_krai': sum(report.qty_books_part_krai for report in book_reports_year),
        'qty_books_reference_do_14': sum(report.qty_books_reference_do_14 for report in book_reports_year),
        'qty_books_reference_14': sum(report.qty_books_reference_14 for report in book_reports_year),
        'qty_books_reference_35': sum(report.qty_books_reference_35 for report in book_reports_year),
        'qty_books_reference_invalid': sum(report.qty_books_reference_invalid for report in book_reports_year),
        'qty_books_reference_online': sum(report.qty_books_reference_online for report in book_reports_year),
    }

    # Записываем данные с начала года в строку 5
    ws['B5'] = (
            year_start_data['qty_books_14'] + year_start_data['qty_books_15_35'] + year_start_data['qty_books_other'] +
            year_start_data['qty_books_neb'] + year_start_data['qty_books_prlib'] +
            year_start_data['qty_books_litres'] + year_start_data['qty_books_consultant'] +
            year_start_data['qty_books_local_library']
    )
    ws['C5'] = year_start_data['qty_books_14']
    ws['D5'] = year_start_data['qty_books_15_35']
    ws['E5'] = year_start_data['qty_books_other']
    ws['F5'] = year_start_data['qty_books_invalid']
    ws['G5'] = year_start_data['qty_books_neb']
    ws['H5'] = year_start_data['qty_books_prlib']
    ws['I5'] = year_start_data['qty_books_litres']
    ws['J5'] = year_start_data['qty_books_consultant']
    ws['K5'] = year_start_data['qty_books_local_library']
    ws['L5'] = (
            year_start_data['qty_books_part_opl'] + year_start_data['qty_books_part_enm'] +
            year_start_data['qty_books_part_tech'] + year_start_data['qty_books_part_sh'] +
            year_start_data['qty_books_part_si'] + year_start_data['qty_books_part_yl'] +
            year_start_data['qty_books_part_hl'] + year_start_data['qty_books_part_dl'] +
            year_start_data['qty_books_part_other'] + year_start_data['qty_books_part_audio'] +
            year_start_data['qty_books_part_krai']
    )
    ws['M5'] = year_start_data['qty_books_part_opl']
    ws['N5'] = year_start_data['qty_books_part_enm']
    ws['O5'] = year_start_data['qty_books_part_tech']
    ws['P5'] = year_start_data['qty_books_part_sh']
    ws['Q5'] = year_start_data['qty_books_part_si']
    ws['R5'] = year_start_data['qty_books_part_yl']
    ws['S5'] = year_start_data['qty_books_part_hl']
    ws['T5'] = year_start_data['qty_books_part_dl']
    ws['U5'] = year_start_data['qty_books_part_other']
    ws['V5'] = year_start_data['qty_books_part_audio']
    ws['W5'] = year_start_data['qty_books_part_krai']
    ws['X5'] = year_start_data['qty_books_reference_do_14'] + year_start_data['qty_books_reference_14'] + year_start_data['qty_books_reference_35']
    ws['Y5'] = year_start_data['qty_books_reference_do_14']
    ws['Z5'] = year_start_data['qty_books_reference_14']
    ws['AA5'] = year_start_data['qty_books_reference_35']
    ws['AB5'] = year_start_data['qty_books_reference_invalid']
    ws['AC5'] = year_start_data['qty_books_reference_online']

    # Заполняем данные за текущий месяц
    current_date = date(year, month, 1)
    month_name_ru = date_format(current_date, "F")
    ws['A1'] = f"Отчет по книговыдаче за {month_name_ru} {year} года"
    ws['U1'] = f"{branch}"

    row_num = 6  # Начинаем с 6 строки (после заголовков)
    for report in book_reports:
        # Вставляем строку перед записью данных (кроме первой строки)
        if row_num > 6:
            ws.insert_rows(row_num)  # Вставляем новую строку
            for col in range(1, ws.max_column + 1):
                ws.cell(row=row_num, column=col)._style = ws.cell(row=6, column=col)._style  # Копируем стили

        # Записываем данные в текущую строку
        ws[f'A{row_num}'] = report.date.strftime('%d.%m.%Y')
        ws[f'B{row_num}'] = (
                report.qty_books_14 + report.qty_books_15_35 + report.qty_books_other + report.qty_books_neb +
                report.qty_books_prlib + report.qty_books_litres + report.qty_books_consultant + report.qty_books_local_library
        )
        ws[f'C{row_num}'] = report.qty_books_14
        ws[f'D{row_num}'] = report.qty_books_15_35
        ws[f'E{row_num}'] = report.qty_books_other
        ws[f'F{row_num}'] = report.qty_books_invalid
        ws[f'G{row_num}'] = report.qty_books_neb
        ws[f'H{row_num}'] = report.qty_books_prlib
        ws[f'I{row_num}'] = report.qty_books_litres
        ws[f'J{row_num}'] = report.qty_books_consultant
        ws[f'K{row_num}'] = report.qty_books_local_library
        ws[f'L{row_num}'] = (
                report.qty_books_part_opl + report.qty_books_part_enm + report.qty_books_part_tech +
                report.qty_books_part_sh + report.qty_books_part_si + report.qty_books_part_yl +
                report.qty_books_part_hl + report.qty_books_part_dl + report.qty_books_part_other +
                report.qty_books_part_audio + report.qty_books_part_krai
        )
        ws[f'M{row_num}'] = report.qty_books_part_opl
        ws[f'N{row_num}'] = report.qty_books_part_enm
        ws[f'O{row_num}'] = report.qty_books_part_tech
        ws[f'P{row_num}'] = report.qty_books_part_sh
        ws[f'Q{row_num}'] = report.qty_books_part_si
        ws[f'R{row_num}'] = report.qty_books_part_yl
        ws[f'S{row_num}'] = report.qty_books_part_hl
        ws[f'T{row_num}'] = report.qty_books_part_dl
        ws[f'U{row_num}'] = report.qty_books_part_other
        ws[f'V{row_num}'] = report.qty_books_part_audio
        ws[f'W{row_num}'] = report.qty_books_part_krai
        ws[f'X{row_num}'] = report.qty_books_reference_do_14 + report.qty_books_reference_14 + report.qty_books_reference_35
        ws[f'Y{row_num}'] = report.qty_books_reference_do_14
        ws[f'Z{row_num}'] = report.qty_books_reference_14
        ws[f'AA{row_num}'] = report.qty_books_reference_35
        ws[f'AB{row_num}'] = report.qty_books_reference_invalid
        ws[f'AC{row_num}'] = report.qty_books_reference_online
        ws[f'AD{row_num}'] = report.note
        row_num += 1

def generate_events_report(wb, branch, year, month):
    ws = wb["Массовые мероприятия"]

    # Фильтруем мероприятия по филиалу, году и месяцу
    events = Event.objects.filter(
        library=branch,
        date__year=year,
        date__month=month
    ).order_by('date')

    # Фильтруем мероприятия с начала года до текущего месяца (не включая текущий месяц)
    events_year = Event.objects.filter(
        library=branch,
        date__year=year,
        date__month__lt=month
    ).order_by('date')

    # Агрегируем данные с начала года
    year_start_data = {
        'quantity': sum(event.quantity for event in events_year),
        'participants': sum(event.age_14 + event.age_35 + event.age_other for event in events_year),
        'age_14': sum(event.age_14 for event in events_year),
        'age_35': sum(event.age_35 for event in events_year),
        'age_other': sum(event.age_other for event in events_year),
        'invalids': sum(event.invalids for event in events_year),
        'pensioners': sum(event.pensioners for event in events_year),
        'out_of_station': sum(event.out_of_station for event in events_year),
    }

    # Записываем данные с начала года в строку 6
    ws['D5'] = year_start_data['quantity']
    ws['E5'] = year_start_data['participants']
    ws['F5'] = year_start_data['age_14']
    ws['G5'] = year_start_data['age_35']
    ws['H5'] = year_start_data['age_other']
    ws['I5'] = year_start_data['invalids']
    ws['J5'] = year_start_data['pensioners']
    ws['K5'] = year_start_data['out_of_station']

    current_date = date(year, month, 1)
    month_name_ru = date_format(current_date, "F")
    # Заполняем данные за текущий месяц
    ws['A1'] = f"Отчет по мероприятиям за {month_name_ru} {year} года"
    ws['G1'] = f"{branch}"

    row_num = 6  # Начинаем с 7 строки (после заголовков)
    for event in events:
        # Вставляем строку перед записью данных (кроме первой строки)
        if row_num > 6:
            ws.insert_rows(row_num)  # Вставляем новую строку
            for col in range(1, ws.max_column + 1):
                ws.cell(row=row_num, column=col)._style = ws.cell(row=6, column=col)._style  # Копируем стили

        # Записываем данные в текущую строку
        ws[f'A{row_num}'] = event.date.strftime('%d.%m.%Y')
        ws[f'B{row_num}'] = event.name
        ws[f'C{row_num}'] = event.direction
        ws[f'D{row_num}'] = event.quantity
        ws[f'E{row_num}'] = event.age_14 + event.age_35 + event.age_other
        ws[f'F{row_num}'] = event.age_14
        ws[f'G{row_num}'] = event.age_35
        ws[f'H{row_num}'] = event.age_other
        ws[f'I{row_num}'] = event.invalids
        ws[f'J{row_num}'] = event.pensioners
        ws[f'K{row_num}'] = event.out_of_station
        ws[f'L{row_num}'] = event.as_part
        ws[f'M{row_num}'] = 'X' if event.paid else ''
        ws[f'N{row_num}'] = event.note
        row_num += 1


def generate_quarter_excel(user, year, quarter):
    try:
        # Получаем филиал текущего пользователя
        branch = Branch.objects.get(id=user.employee.branch.id)
    except AttributeError:
        return None  # Если пользователь не связан с сотрудником

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, 'reports/excell/report_quarter_template.xlsx')

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"File not found: {template_path}")

    wb = openpyxl.load_workbook(filename=template_path)
    ws = wb.active

    # Заполняем шапку отчета
    ws['E3'] = f'Значение показателя в {quarter} квартале {year} года'
    ws['C3'] = f'Данные статистики по посещаемости по итогам {year - 1} года'
    ws['D3'] = f'Значение целевого показателя за {year} год план'
    ws['B7'] = branch.full_name

    # Заполняем данные за предыдущий год
    previous_year_data = (
        VisitReport.objects.filter(library=branch, date__year=year - 1).aggregate(
            total_visited_14=models.Sum('qty_visited_14'),
            total_visited_15_35=models.Sum('qty_visited_15_35'),
            total_visited_other=models.Sum('qty_visited_other'),
            total_visited_online=models.Sum('qty_visited_online'),
            total_visited_prlib=models.Sum('qty_visited_prlib'),
            total_visited_litres=models.Sum('qty_visited_litres'),
            total_visited_out_station=models.Sum('qty_visited_out_station'),
        )
    )

    event_data = (
        Event.objects.filter(library=branch, date__year=year - 1).aggregate(
            total_age_14=models.Sum('age_14'),
            total_age_35=models.Sum('age_35'),
            total_age_other=models.Sum('age_other'),
            total_online=models.Sum('online'),
            total_out_of_station=models.Sum('out_of_station'),
        )
    )

    for key, value in previous_year_data.items():
        if value is None:
            previous_year_data[key] = 0

    for key, value in event_data.items():
        if value is None:
            event_data[key] = 0

    if previous_year_data['total_visited_14'] is not None:
        ws['C7'] = (
                previous_year_data['total_visited_14'] +
                previous_year_data['total_visited_15_35'] +
                previous_year_data['total_visited_other'] +
                event_data['total_age_14'] +
                event_data['total_age_35'] +
                event_data['total_age_other'] +
                event_data['total_online'] +
                previous_year_data['total_visited_online'] +
                previous_year_data['total_visited_prlib'] +
                previous_year_data['total_visited_litres'] +
                event_data['total_out_of_station'] +
                previous_year_data['total_visited_out_station']
        )
    else:
        visits_first_data = VisitsFirstData.objects.filter(library=branch).first()
        events_first_data = EventsFirstData.objects.filter(library=branch).first()
        ws['C7'] = (visits_first_data.data if visits_first_data else 0) + (events_first_data.data if events_first_data else 0)

    # Заполняем плановые показатели за текущий год
    visit_plan = VisitPlan.objects.filter(library=branch, year=year).first()
    events_plan = EventsPlan.objects.filter(library=branch, year=year).first()
    ws['D7'] = (visit_plan.total_visits if visit_plan else 0) + (events_plan.total_events if events_plan else 0)

    # Заполняем данные за выбранный квартал
    months = {
        1: ['январь', 'февраль', 'март'],
        2: ['апрель', 'май', 'июнь'],
        3: ['июль', 'август', 'сентябрь'],
        4: ['октябрь', 'ноябрь', 'декабрь'],
    }

    for i, month in enumerate(months[quarter]):
        month_index = i * 6 + 5  # Смещение для каждого месяца
        ws[f'E{4 + i * 6}'] = f'{month} посещаемость (всего)'

        # Заполняем данные за месяц
        visit_report = VisitReport.objects.filter(library=branch, date__year=year, date__month=quarter * 3 - 2 + i).first()
        event_data_month = Event.objects.filter(library=branch, date__year=year, date__month=quarter * 3 - 2 + i).first()

        if visit_report and event_data_month:
            ws[f'E{7 + i * 6}'] = (
                    (visit_report.qty_visited_14 or 0) +
                    (visit_report.qty_visited_15_35 or 0) +
                    (visit_report.qty_visited_other or 0) +
                    (event_data_month.age_14 or 0) +
                    (event_data_month.age_35 or 0) +
                    (event_data_month.age_other or 0)
            )
            ws[f'F{7 + i * 6}'] = (
                    (event_data_month.age_14 or 0) +
                    (event_data_month.age_35 or 0) +
                    (event_data_month.age_other or 0)
            )
            ws[f'G{7 + i * 6}'] = (
                    (event_data_month.online or 0) +
                    (visit_report.qty_visited_online or 0) +
                    (visit_report.qty_visited_prlib or 0) +
                    (visit_report.qty_visited_litres or 0)
            )
            ws[f'H{7 + i * 6}'] = (
                    (event_data_month.out_of_station or 0) +
                    (visit_report.qty_visited_out_station or 0)
            )
            ws[f'I{7 + i * 6}'] = event_data_month.out_of_station or 0
            ws[f'J{7 + i * 6}'] = ws[f'E{7 + i * 6}'].value + ws[f'G{7 + i * 6}'].value + ws[f'H{7 + i * 6}'].value
        else:
            # Если данные отсутствуют, заполняем нулями
            ws[f'E{7 + i * 6}'] = 0
            ws[f'F{7 + i * 6}'] = 0
            ws[f'G{7 + i * 6}'] = 0
            ws[f'H{7 + i * 6}'] = 0
            ws[f'I{7 + i * 6}'] = 0
            ws[f'J{7 + i * 6}'] = 0

    # Заполняем итоговые данные
    ws['W7'] = ws['V7'].value + ws['P7'].value + ws['J7'].value

    # Заполняем процент выполнения плана
    if ws['D7'].value != 0:
        ws['Y7'] = (ws['X7'].value / ws['D7'].value) * 100

    # Сохраняем файл
    filename = f"quarter_report_{quarter}_quarter_{year}.xlsx"
    safe_filename = quote(filename)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
    wb.save(response)
    return response
