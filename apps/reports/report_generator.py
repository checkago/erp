import os
import locale
from babel.dates import format_datetime
import calendar
from urllib.parse import quote
import openpyxl
from django.conf.locale import ru
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.utils.formats import date_format
from openpyxl import load_workbook
from django.utils import translation, timezone
from .models import VisitReport, BookReport, Event, VisitsFirstData, EventsFirstData, VisitPlan, EventsPlan, RegsPlan, \
    BookPlan
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
    filename = f"эл.дневник_{branch.short_name}_{year}_{month_name}.xlsx"
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
        'qty_reg_out_of_station': sum(report.qty_reg_out_of_station for report in visit_reports_year),
        'qty_reg_prlib': sum(report.qty_reg_prlib for report in visit_reports_year),
        'qty_reg_litres': sum(report.qty_reg_litres for report in visit_reports_year),
        'qty_visited_14': sum(report.qty_visited_14 for report in visit_reports_year),
        'qty_visited_15_35': sum(report.qty_visited_15_35 for report in visit_reports_year),
        'qty_visited_other': sum(report.qty_visited_other for report in visit_reports_year),
        'qty_visited_pensioners': sum(report.qty_visited_pensioners for report in visit_reports_year),
        'qty_visited_invalids': sum(report.qty_visited_invalids for report in visit_reports_year),
        'qty_visited_out_station': sum(report.qty_visited_out_station for report in visit_reports_year),
        'qty_visited_prlib': sum(report.qty_visited_prlib for report in visit_reports_year),
        'qty_visited_litres': sum(report.qty_visited_litres for report in visit_reports_year),
        'qty_visited_online': sum(report.qty_visited_online for report in visit_reports_year),
    }

    # Записываем данные с начала года в строку 6
    ws['B6'] = year_start_data['qty_reg_14'] + year_start_data['qty_reg_15_35'] + year_start_data['qty_reg_other']
    ws['C6'] = year_start_data['qty_reg_14']
    ws['D6'] = year_start_data['qty_reg_15_35']
    ws['E6'] = year_start_data['qty_reg_other']
    ws['F6'] = year_start_data['qty_reg_pensioners']
    ws['G6'] = year_start_data['qty_reg_invalid']
    ws['H6'] = year_start_data['qty_reg_out_of_station']
    ws['I6'] = year_start_data['qty_reg_prlib']
    ws['J6'] = year_start_data['qty_reg_litres']
    ws['K6'] = year_start_data['qty_visited_14'] + year_start_data['qty_visited_15_35'] + year_start_data['qty_visited_other']
    ws['L6'] = year_start_data['qty_visited_14']
    ws['M6'] = year_start_data['qty_visited_15_35']
    ws['N6'] = year_start_data['qty_visited_other']
    ws['O6'] = year_start_data['qty_visited_pensioners']
    ws['P6'] = year_start_data['qty_visited_invalids']
    ws['QP6'] = year_start_data['qty_visited_out_station']
    ws['R6'] = year_start_data['qty_visited_prlib']
    ws['S6'] = year_start_data['qty_visited_litres']
    ws['T6'] = year_start_data['qty_visited_online']

    # Заполняем данные за текущий месяц
    current_date = date(year, month, 1)
    month_name_ru = date_format(current_date, "F")
    ws['A1'] = f"Отчет по посещениям за {month_name_ru} {year} года"
    ws['O1'] = f"{branch}"

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
        ws[f'H{row_num}'] = report.qty_reg_out_of_station
        ws[f'I{row_num}'] = report.qty_reg_prlib
        ws[f'J{row_num}'] = report.qty_reg_litres
        ws[f'K{row_num}'] = report.qty_visited_14 + report.qty_visited_15_35 + report.qty_visited_other
        ws[f'L{row_num}'] = report.qty_visited_14
        ws[f'M{row_num}'] = report.qty_visited_15_35
        ws[f'N{row_num}'] = report.qty_visited_other
        ws[f'O{row_num}'] = report.qty_visited_pensioners
        ws[f'P{row_num}'] = report.qty_visited_invalids
        ws[f'Q{row_num}'] = report.qty_visited_out_station
        ws[f'R{row_num}'] = report.qty_visited_prlib
        ws[f'S{row_num}'] = report.qty_visited_litres
        ws[f'T{row_num}'] = report.qty_visited_online
        ws[f'U{row_num}'] = report.note
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
        'qty_books_out_of_station': sum(report.qty_books_out_of_station for report in book_reports_year),
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
    ws['G5'] = year_start_data['qty_books_out_of_station']
    ws['H5'] = year_start_data['qty_books_neb']
    ws['I5'] = year_start_data['qty_books_prlib']
    ws['J5'] = year_start_data['qty_books_litres']
    ws['K5'] = year_start_data['qty_books_consultant']
    ws['L5'] = year_start_data['qty_books_local_library']
    ws['M5'] = (
            year_start_data['qty_books_part_opl'] + year_start_data['qty_books_part_enm'] +
            year_start_data['qty_books_part_tech'] + year_start_data['qty_books_part_sh'] +
            year_start_data['qty_books_part_si'] + year_start_data['qty_books_part_yl'] +
            year_start_data['qty_books_part_hl'] + year_start_data['qty_books_part_dl'] +
            year_start_data['qty_books_part_other'] + year_start_data['qty_books_part_audio'] +
            year_start_data['qty_books_part_krai']
    )
    ws['N5'] = year_start_data['qty_books_part_opl']
    ws['O5'] = year_start_data['qty_books_part_enm']
    ws['P5'] = year_start_data['qty_books_part_tech']
    ws['Q5'] = year_start_data['qty_books_part_sh']
    ws['R5'] = year_start_data['qty_books_part_si']
    ws['S5'] = year_start_data['qty_books_part_yl']
    ws['T5'] = year_start_data['qty_books_part_hl']
    ws['U5'] = year_start_data['qty_books_part_dl']
    ws['V5'] = year_start_data['qty_books_part_other']
    ws['W5'] = year_start_data['qty_books_part_audio']
    ws['X5'] = year_start_data['qty_books_part_krai']
    ws['Y5'] = year_start_data['qty_books_reference_do_14'] + year_start_data['qty_books_reference_14'] + year_start_data['qty_books_reference_35']
    ws['Z5'] = year_start_data['qty_books_reference_do_14']
    ws['AA5'] = year_start_data['qty_books_reference_14']
    ws['AB5'] = year_start_data['qty_books_reference_35']
    ws['AC5'] = year_start_data['qty_books_reference_invalid']
    ws['AD5'] = year_start_data['qty_books_reference_online']

    # Заполняем данные за текущий месяц
    current_date = date(year, month, 1)
    month_name_ru = date_format(current_date, "F")
    ws['A1'] = f"Отчет по книговыдаче за {month_name_ru} {year} года"
    ws['V1'] = f"{branch}"

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
        ws[f'G{row_num}'] = report.qty_books_out_of_station
        ws[f'H{row_num}'] = report.qty_books_neb
        ws[f'I{row_num}'] = report.qty_books_prlib
        ws[f'J{row_num}'] = report.qty_books_litres
        ws[f'K{row_num}'] = report.qty_books_consultant
        ws[f'L{row_num}'] = report.qty_books_local_library
        ws[f'M{row_num}'] = (
                report.qty_books_part_opl + report.qty_books_part_enm + report.qty_books_part_tech +
                report.qty_books_part_sh + report.qty_books_part_si + report.qty_books_part_yl +
                report.qty_books_part_hl + report.qty_books_part_dl + report.qty_books_part_other +
                report.qty_books_part_audio + report.qty_books_part_krai
        )
        ws[f'N{row_num}'] = report.qty_books_part_opl
        ws[f'O{row_num}'] = report.qty_books_part_enm
        ws[f'P{row_num}'] = report.qty_books_part_tech
        ws[f'Q{row_num}'] = report.qty_books_part_sh
        ws[f'R{row_num}'] = report.qty_books_part_si
        ws[f'S{row_num}'] = report.qty_books_part_yl
        ws[f'T{row_num}'] = report.qty_books_part_hl
        ws[f'U{row_num}'] = report.qty_books_part_dl
        ws[f'V{row_num}'] = report.qty_books_part_other
        ws[f'W{row_num}'] = report.qty_books_part_audio
        ws[f'X{row_num}'] = report.qty_books_part_krai
        ws[f'Y{row_num}'] = report.qty_books_reference_do_14 + report.qty_books_reference_14 + report.qty_books_reference_35
        ws[f'Z{row_num}'] = report.qty_books_reference_do_14
        ws[f'AA{row_num}'] = report.qty_books_reference_14
        ws[f'AB{row_num}'] = report.qty_books_reference_35
        ws[f'AC{row_num}'] = report.qty_books_reference_invalid
        ws[f'AD{row_num}'] = report.qty_books_reference_online
        ws[f'AE{row_num}'] = report.note
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
        employee = Employee.objects.get(user=user)
        branch = employee.branch
    except Employee.DoesNotExist:
        return None

    if not branch:
        return None

    # Устанавливаем русскую локаль только для этого потока
    old_locale = locale.getlocale()
    try:
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    except locale.Error:
        # Если не удалось установить локаль, используем fallback
        pass

    # Загрузка шаблона
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, 'reports/excell/report_quarter_template.xlsx')

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"File not found: {template_path}")

    wb = load_workbook(filename=template_path)
    ws = wb.active

    # Динамическое заполнение заголовков
    ws['E3'] = f"Значение показателя в {quarter} квартале {year} года"
    ws['C3'] = f"Данные статистики по посещаемости по итогам {year - 1} года"
    ws['D3'] = f"Значение целевого показателя за {year} год план"
    ws['W3'] = f"итого за {quarter}-й квартал {year}"

    # Полное наименование филиала
    ws['B7'] = branch.full_name

    # Данные за предыдущий год
    previous_year = year - 1
    total_prev_year = get_total_previous_year(branch, previous_year)
    ws['C7'] = total_prev_year

    # Плановые показатели за текущий год
    total_plan = get_total_plan(branch, year)
    ws['D7'] = total_plan

    # Данные за выбранный квартал
    months = {
        1: (1, 2, 3),
        2: (4, 5, 6),
        3: (7, 8, 9),
        4: (10, 11, 12)
    }[quarter]

    # Заполнение данных по месяцам
    for i, month in enumerate(months):
        col_offset = i * 6
        fill_month_data(ws, branch, year, month, col_offset)

    # Итог за квартал
    total_quarter = 0
    for i, month in enumerate(months):
        col_offset = i * 6
        total_quarter += (ws[f'{chr(74 + col_offset)}7'].value or 0)

    ws['W7'] = total_quarter

    # Итог за год
    total_year = get_total_year(branch, year)
    ws['X7'] = total_year

    # Процент выполнения плана
    ws['Y7'] = (ws['X7'].value / (ws['D7'].value or 1)) * 100 if ws['X7'].value is not None else 0

    # Динамическое заполнение названий месяцев
    month_names = []
    for month in months:
        current_date = datetime(year, month, 1)
        month_name_ru = date_format(current_date, "F")
        month_names.append(month_name_ru)

    ws['E4'] = f"{month_names[0]} посещаемость (всего)"
    if len(months) > 1:
        ws['K4'] = f"{month_names[1]} посещаемость (всего)"
    if len(months) > 2:
        ws['Q4'] = f"{month_names[2]} посещаемость (всего)"

    # Возвращаем язык по умолчанию
    translation.deactivate()

    # Сохранение файла
    filename = f"квартальный_нац_цели_{branch.short_name}_{year}_Q{quarter}.xlsx"
    safe_filename = quote(filename)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
    wb.save(response)
    return response

def get_total_previous_year(branch, previous_year):
    visit_reports_prev_year = VisitReport.objects.filter(library=branch, date__year=previous_year)
    events_prev_year = Event.objects.filter(library=branch, date__year=previous_year)

    total_visits_prev_year = sum(
        (report.qty_visited_14 or 0) + (report.qty_visited_15_35 or 0) + (report.qty_visited_other or 0)
        for report in visit_reports_prev_year
    )

    total_events_prev_year = sum(
        (event.age_14 or 0) + (event.age_35 or 0) + (event.age_other or 0)
        for event in events_prev_year
    )

    total_online_prev_year = sum(
        (event.online or 0) for event in events_prev_year
    ) + sum(
        (report.qty_visited_online or 0) + (report.qty_visited_prlib or 0) + (report.qty_visited_litres or 0)
        for report in visit_reports_prev_year
    )

    total_out_station_prev_year = sum(
        (event.out_of_station or 0) for event in events_prev_year
    ) + sum(
        (report.qty_visited_out_station or 0)
        for report in visit_reports_prev_year
    )

    total_prev_year = (
            total_visits_prev_year +
            total_events_prev_year +
            total_online_prev_year +
            total_out_station_prev_year
    )

    if not visit_reports_prev_year.exists() and not events_prev_year.exists():
        visits_first_data = VisitsFirstData.objects.filter(library=branch).first()
        events_first_data = EventsFirstData.objects.filter(library=branch).first()
        total_prev_year = ((visits_first_data.data or 0) if visits_first_data else 0) + (
            (events_first_data.data or 0) if events_first_data else 0)

    return total_prev_year

def get_total_plan(branch, year):
    visit_plan = VisitPlan.objects.filter(library=branch, year=year).first()
    events_plan = EventsPlan.objects.filter(library=branch, year=year).first()
    total_plan = ((visit_plan.total_visits or 0) if visit_plan else 0) + ((events_plan.total_events or 0) if events_plan else 0)
    return total_plan

def fill_month_data(ws, branch, year, month, col_offset):
    visit_reports = VisitReport.objects.filter(library=branch, date__year=year, date__month=month)
    events = Event.objects.filter(library=branch, date__year=year, date__month=month)

    total_visits = sum(
        (report.qty_visited_14 or 0) + (report.qty_visited_15_35 or 0) + (report.qty_visited_other or 0) - (report.qty_visited_out_station or 0)
        for report in visit_reports
    )
    total_events = sum(
        (event.age_14 or 0) + (event.age_35 or 0) + (event.age_other or 0) - (event.out_of_station or 0)
        for event in events
    )
    total_online = sum(
        (event.online or 0) for event in events
    ) + sum(
        (report.qty_visited_online or 0) + (report.qty_visited_prlib or 0) + (report.qty_visited_litres or 0)
        for report in visit_reports
    )
    total_out_station = sum(
        (event.out_of_station or 0) for event in events
    ) + sum(
        (report.qty_visited_out_station or 0)
        for report in visit_reports
    )
    total_events_out_station = sum(
        (event.out_of_station or 0) for event in events
    )

    # Записываем данные в ячейки
    ws[f'{chr(69 + col_offset)}7'] = total_visits + total_events
    ws[f'{chr(70 + col_offset)}7'] = total_events
    ws[f'{chr(71 + col_offset)}7'] = total_online
    ws[f'{chr(72 + col_offset)}7'] = total_out_station
    ws[f'{chr(73 + col_offset)}7'] = total_events_out_station
    ws[f'{chr(74 + col_offset)}7'] = (ws[f'{chr(69 + col_offset)}7'].value or 0) + (ws[f'{chr(71 + col_offset)}7'].value or 0) + (ws[f'{chr(72 + col_offset)}7'].value or 0)

def get_total_year(branch, year):
    visit_reports_year = VisitReport.objects.filter(library=branch, date__year=year)
    events_year = Event.objects.filter(library=branch, date__year=year)
    total_year = (
        sum((report.qty_visited_14 or 0) + (report.qty_visited_15_35 or 0) + (report.qty_visited_other or 0) for report in visit_reports_year) +
        sum((event.age_14 or 0) + (event.age_35 or 0) + (event.age_other or 0) for event in events_year) +
        sum((event.online or 0) + (report.qty_visited_online or 0) + (report.qty_visited_prlib or 0) + (report.qty_visited_litres or 0) for event, report in zip(events_year, visit_reports_year)) +
        sum((event.out_of_station or 0) + (report.qty_visited_out_station or 0) for event, report in zip(events_year, visit_reports_year))
    )
    return total_year

    # Процент выполнения плана
    ws['Y7'] = ws['X7'].value / (ws['D7'].value / 100) if ws['D7'].value else 0

    # Получаем названия месяцев
    month_names = [format_datetime(datetime(year, month, 1), 'MMMM', locale='ru') for month in months]

    # Записываем названия месяцев в ячейки Excel
    ws['E4'] = f"{month_names[1]} посещаемость (всего)" if len(month_names) >= 1 else ""
    ws['K4'] = f"{month_names[2]} посещаемость (всего)" if len(month_names) >= 2 else ""
    ws['Q4'] = f"{month_names[3]} посещаемость (всего)" if len(month_names) >= 3 else ""


    # Сохранение файла
    filename = f"квартальный_нац_цели_{branch.short_name}_{year}_Q{quarter}.xlsx"
    safe_filename = quote(filename)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
    wb.save(response)
    return response


def generate_digital_month_report(user, month):
    try:
        employee = Employee.objects.get(user=user)
        branch = employee.branch
    except Employee.DoesNotExist:
        return None

    if not branch:
        return None

    # Автоматическое определение текущего года
    current_year = datetime.now().year

    # Загрузка шаблона
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, 'reports/excell/digital_month_template.xlsx')

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"File not found: {template_path}")

    wb = load_workbook(filename=template_path)
    ws = wb.active

    # Заполнение заголовка
    current_date = date(current_year, month, 1)
    month_name = date_format(current_date, "F")
    ws['A1'] = f"Цифровой отчёт о работе {branch.full_name} (МБУК «ЦБС им. А. Белого» Балашиха) за {month_name} {current_year} года (с нарастающим итогом)"

    # Получаем данные за текущий год до конца выбранного месяца
    visit_reports = VisitReport.objects.filter(library=branch, date__year=current_year, date__month__lte=month)
    book_reports = BookReport.objects.filter(library=branch, date__year=current_year, date__month__lte=month)
    events = Event.objects.filter(library=branch, date__year=current_year, date__month__lte=month)

    # Плановые показатели
    regs_plan = RegsPlan.objects.filter(library=branch, year=current_year).first()
    book_plan = BookPlan.objects.filter(library=branch, year=current_year).first()
    visit_plan = VisitPlan.objects.filter(library=branch, year=current_year).first()

    # Заполнение данных
    ws['B4'] = regs_plan.total_regs if regs_plan else 0
    ws['C4'] = sum(
        (report.qty_reg_14 or 0) + (report.qty_reg_15_35 or 0) + (report.qty_reg_other or 0) +
        (report.qty_reg_prlib or 0) + (report.qty_reg_litres or 0) + (report.qty_reg_out_of_station or 0)
        for report in visit_reports
    )
    ws['D4'] = (ws['C4'].value / ws['B4'].value) * 100 if ws['B4'].value else 0

    ws['C5'] = sum(report.qty_reg_14 or 0 for report in visit_reports)
    ws['C6'] = sum(report.qty_reg_15_35 or 0 for report in visit_reports)
    ws['C7'] = sum((report.qty_reg_14 or 0) + (report.qty_reg_15_35 or 0) + (report.qty_reg_other or 0) for report in visit_reports)
    ws['C8'] = sum(report.qty_reg_out_of_station or 0 for report in visit_reports)
    ws['C9'] = sum((report.qty_reg_prlib or 0) + (report.qty_reg_litres or 0) for report in visit_reports)

    ws['B10'] = book_plan.total_books if book_plan else 0
    ws['C10'] = sum(
        (report.qty_books_14 or 0) + (report.qty_books_15_35 or 0) + (report.qty_books_other or 0) +
        (report.qty_books_neb or 0) + (report.qty_books_prlib or 0) + (report.qty_books_litres or 0) +
        (report.qty_books_consultant or 0) + (report.qty_books_local_library or 0) + (report.qty_books_out_of_station or 0)
        for report in book_reports
    )
    ws['D10'] = (ws['C10'].value / ws['B10'].value) * 100 if ws['B10'].value else 0

    ws['C11'] = sum(report.qty_books_14 or 0 for report in book_reports)
    ws['C12'] = sum(report.qty_books_15_35 or 0 for report in book_reports)
    ws['C13'] = sum((report.qty_books_14 or 0) + (report.qty_books_15_35 or 0) + (report.qty_books_other or 0) for report in book_reports)
    ws['C14'] = sum(report.qty_books_out_of_station or 0 for report in book_reports)
    ws['C15'] = sum(
        (report.qty_books_neb or 0) + (report.qty_books_prlib or 0) + (report.qty_books_litres or 0) +
        (report.qty_books_consultant or 0) + (report.qty_books_local_library or 0)
        for report in book_reports
    )

    ws['B16'] = visit_plan.total_visits if visit_plan else 0
    ws['C16'] = sum(
        (report.qty_visited_14 or 0) + (report.qty_visited_15_35 or 0) + (report.qty_visited_other or 0) + (report.qty_visited_out_station or 0) +
        (report.qty_visited_online or 0) + (report.qty_visited_prlib or 0) + (report.qty_visited_litres or 0) +
        (event.age_14 or 0) + (event.age_35 or 0) + (event.age_other or 0) + (event.online or 0)
        for report, event in zip(visit_reports, events)
    )
    ws['D16'] = (ws['C16'].value / ws['B16'].value) * 100 if ws['B16'].value else 0

    ws['C17'] = sum((report.qty_visited_14 or 0) + (event.age_14 or 0) for report, event in zip(visit_reports, events))
    ws['C18'] = sum((report.qty_visited_15_35 or 0) + (event.age_35 or 0) for report, event in zip(visit_reports, events))
    ws['C19'] = sum((report.qty_visited_14 or 0) + (report.qty_visited_15_35 or 0) + (report.qty_visited_other or 0) for report in visit_reports)
    ws['C20'] = sum(report.qty_visited_out_station or 0 for report in visit_reports)
    ws['C21'] = sum((report.qty_visited_online or 0) + (report.qty_visited_prlib or 0) + (report.qty_visited_litres or 0) for report in visit_reports)
    ws['C22'] = sum((report.qty_visited_invalids or 0) + (event.invalids or 0) for report, event in zip(visit_reports, events))
    ws['C23'] = sum((event.age_14 or 0) + (event.age_35 or 0) + (event.age_other or 0) for event in events if event.paid)
    ws['C24'] = sum(event.invalids or 0 for event in events if event.paid)
    ws['C25'] = sum((report.qty_books_reference_online or 0) + (report.qty_books_reference_do_14 or 0) + (
                report.qty_books_reference_14 or 0) +
                    + (report.qty_books_reference_35 or 0) for report in book_reports)
    ws['C26'] = sum(report.qty_books_reference_do_14 or 0 for report in book_reports)
    ws['C27'] = sum(report.qty_books_reference_14 or 0 for report in book_reports)
    ws['C28'] = sum(report.qty_books_reference_online or 0 for report in book_reports)

    ws['C29'] = sum(event.quantity or 0 for event in events)
    ws['C30'] = sum((event.age_14 or 0) + (event.age_35 or 0) + (event.age_other or 0) for event in events)

    ws['C31'] = sum(event.quantity or 0 for event in events if event.age_14 != 0)
    ws['C32'] = sum(event.age_14 or 0 for event in events if event.age_14 != 0)
    ws['C33'] = sum(event.quantity or 0 for event in events if event.age_35 != 0)
    ws['C34'] = sum(event.age_35 or 0 for event in events if event.age_35 != 0)
    ws['C35'] = sum(event.quantity or 0 for event in events if event.out_of_station == 0)
    ws['C36'] = sum((event.age_14 or 0) + (event.age_35 or 0) + (event.age_other or 0) for event in events if event.out_of_station == 0)
    ws['C37'] = sum(event.quantity or 0 for event in events if event.age_14 != 0 and event.out_of_station == 0)
    ws['C38'] = sum(event.age_14 or 0 for event in events if event.age_14 != 0 and event.out_of_station == 0)
    ws['C39'] = sum(event.quantity or 0 for event in events if event.age_35 != 0 and event.out_of_station == 0)
    ws['C40'] = sum(event.age_35 or 0 for event in events if event.age_35 != 0 and event.out_of_station == 0)
    ws['C41'] = sum(event.quantity or 0 for event in events if event.out_of_station != 0)
    ws['C42'] = sum((event.age_14 or 0) + (event.age_35 or 0) + (event.age_other or 0) for event in events if event.out_of_station != 0)

    # Сохранение файла
    filename = f"цифровой_ежемесячный_{branch.short_name}_{current_year}_{month}.xlsx"
    safe_filename = quote(filename)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
    wb.save(response)
    return response