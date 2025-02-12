import os
import openpyxl
from django.http import HttpResponse
from .models import VisitReport, BookReport
from apps.core.models import Employee, Branch
from datetime import datetime

def generate_visit_report_excel(user, year, month):
    # Получаем сотрудника и филиал
    try:
        employee = Employee.objects.get(user=user)
        branch = employee.branch
    except Employee.DoesNotExist:
        return None

    if not branch:
        return None

    # Фильтруем отчеты по филиалу, году и месяцу (текущий месяц)
    visit_reports_current_month = VisitReport.objects.filter(
        library=branch,
        date__year=year,
        date__month=month
    ).order_by('date')

    # Фильтруем отчеты с начала года до текущего месяца (включая текущий месяц)
    visit_reports_since_year_start = VisitReport.objects.filter(
        library=branch,
        date__year=year,
        date__month__lte=month  # Все месяцы с начала года до текущего
    ).order_by('date')

    # Загружаем шаблон
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, 'reports/excell/reg_visited_template.xlsx')

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"File not found: {template_path}")

    wb = openpyxl.load_workbook(filename=template_path)
    ws = wb.active

    # Устанавливаем год в заголовке
    ws['L1'] = f"{year} г."

    # Словарь для агрегации данных по дням (текущий месяц)
    daily_data = {}

    # Словарь для агрегации данных с начала года (включая текущий месяц)
    year_start_data = {
        'qty_reg_14': 0,
        'qty_reg_15_35': 0,
        'qty_reg_other': 0,
        'qty_reg_pensioners': 0,
        'qty_reg_invalid': 0,
        'qty_visited_14': 0,
        'qty_visited_15_35': 0,
        'qty_visited_other': 0,
        'qty_visited_pensioners': 0,
        'qty_visited_invalids': 0,
        'qty_visited_out_station': 0,
        'qty_visited_online': 0,
        'note': ''
    }

    # Словарь для агрегации данных за текущий месяц
    current_month_data = {
        'qty_reg_14': 0,
        'qty_reg_15_35': 0,
        'qty_reg_other': 0,
        'qty_reg_pensioners': 0,
        'qty_reg_invalid': 0,
        'qty_visited_14': 0,
        'qty_visited_15_35': 0,
        'qty_visited_other': 0,
        'qty_visited_pensioners': 0,
        'qty_visited_invalids': 0,
        'qty_visited_out_station': 0,
        'qty_visited_online': 0,
        'note': ''
    }

    # Агрегируем данные по дням (текущий месяц)
    for report in visit_reports_current_month:
        date_key = report.date.day
        if date_key not in daily_data:
            daily_data[date_key] = {
                'qty_reg_14': 0,
                'qty_reg_15_35': 0,
                'qty_reg_other': 0,
                'qty_reg_pensioners': 0,
                'qty_reg_invalid': 0,
                'qty_visited_14': 0,
                'qty_visited_15_35': 0,
                'qty_visited_other': 0,
                'qty_visited_pensioners': 0,
                'qty_visited_invalids': 0,
                'qty_visited_out_station': 0,
                'qty_visited_online': 0,
                'note': ''
            }
        daily_data[date_key]['qty_reg_14'] += report.qty_reg_14
        daily_data[date_key]['qty_reg_15_35'] += report.qty_reg_15_35
        daily_data[date_key]['qty_reg_other'] += report.qty_reg_other
        daily_data[date_key]['qty_reg_pensioners'] += report.qty_reg_pensioners
        daily_data[date_key]['qty_reg_invalid'] += report.qty_reg_invalid
        daily_data[date_key]['qty_visited_14'] += report.qty_visited_14
        daily_data[date_key]['qty_visited_15_35'] += report.qty_visited_15_35
        daily_data[date_key]['qty_visited_other'] += report.qty_visited_other
        daily_data[date_key]['qty_visited_pensioners'] += report.qty_visited_pensioners
        daily_data[date_key]['qty_visited_invalids'] += report.qty_visited_invalids
        daily_data[date_key]['qty_visited_out_station'] += report.qty_visited_out_station
        daily_data[date_key]['qty_visited_online'] += report.qty_visited_online
        daily_data[date_key]['note'] += report.note + " " if report.note else ""

        # Собираем данные за текущий месяц
        current_month_data['qty_reg_14'] += report.qty_reg_14
        current_month_data['qty_reg_15_35'] += report.qty_reg_15_35
        current_month_data['qty_reg_other'] += report.qty_reg_other
        current_month_data['qty_reg_pensioners'] += report.qty_reg_pensioners
        current_month_data['qty_reg_invalid'] += report.qty_reg_invalid
        current_month_data['qty_visited_14'] += report.qty_visited_14
        current_month_data['qty_visited_15_35'] += report.qty_visited_15_35
        current_month_data['qty_visited_other'] += report.qty_visited_other
        current_month_data['qty_visited_pensioners'] += report.qty_visited_pensioners
        current_month_data['qty_visited_invalids'] += report.qty_visited_invalids
        current_month_data['qty_visited_out_station'] += report.qty_visited_out_station
        current_month_data['qty_visited_online'] += report.qty_visited_online
        current_month_data['note'] += report.note + " " if report.note else ""

    # Агрегируем данные с начала года (включая текущий месяц)
    for report in visit_reports_since_year_start:
        year_start_data['qty_reg_14'] += report.qty_reg_14
        year_start_data['qty_reg_15_35'] += report.qty_reg_15_35
        year_start_data['qty_reg_other'] += report.qty_reg_other
        year_start_data['qty_reg_pensioners'] += report.qty_reg_pensioners
        year_start_data['qty_reg_invalid'] += report.qty_reg_invalid
        year_start_data['qty_visited_14'] += report.qty_visited_14
        year_start_data['qty_visited_15_35'] += report.qty_visited_15_35
        year_start_data['qty_visited_other'] += report.qty_visited_other
        year_start_data['qty_visited_pensioners'] += report.qty_visited_pensioners
        year_start_data['qty_visited_invalids'] += report.qty_visited_invalids
        year_start_data['qty_visited_out_station'] += report.qty_visited_out_station
        year_start_data['qty_visited_online'] += report.qty_visited_online
        year_start_data['note'] += report.note + " " if report.note else ""

    # Вычитаем данные за текущий месяц из итогов с начала года
    year_start_data['qty_reg_14'] -= current_month_data['qty_reg_14']
    year_start_data['qty_reg_15_35'] -= current_month_data['qty_reg_15_35']
    year_start_data['qty_reg_other'] -= current_month_data['qty_reg_other']
    year_start_data['qty_reg_pensioners'] -= current_month_data['qty_reg_pensioners']
    year_start_data['qty_reg_invalid'] -= current_month_data['qty_reg_invalid']
    year_start_data['qty_visited_14'] -= current_month_data['qty_visited_14']
    year_start_data['qty_visited_15_35'] -= current_month_data['qty_visited_15_35']
    year_start_data['qty_visited_other'] -= current_month_data['qty_visited_other']
    year_start_data['qty_visited_pensioners'] -= current_month_data['qty_visited_pensioners']
    year_start_data['qty_visited_invalids'] -= current_month_data['qty_visited_invalids']
    year_start_data['qty_visited_out_station'] -= current_month_data['qty_visited_out_station']
    year_start_data['qty_visited_online'] -= current_month_data['qty_visited_online']
    year_start_data['note'] = ""  # Примечания не суммируются

    # Записываем данные с начала года (без текущего месяца) в строку 6
    ws['B6'] = year_start_data['qty_reg_14'] + year_start_data['qty_reg_15_35'] + year_start_data['qty_reg_other']
    ws['C6'] = year_start_data['qty_reg_14']
    ws['D6'] = year_start_data['qty_reg_15_35']
    ws['E6'] = year_start_data['qty_reg_other']
    ws['F6'] = year_start_data['qty_reg_pensioners']
    ws['G6'] = year_start_data['qty_reg_invalid']
    ws['H6'] = year_start_data['qty_visited_14'] + year_start_data['qty_visited_15_35'] + year_start_data['qty_visited_other'] + year_start_data['qty_visited_online']
    ws['I6'] = year_start_data['qty_visited_14']
    ws['J6'] = year_start_data['qty_visited_15_35']
    ws['K6'] = year_start_data['qty_visited_other']
    ws['L6'] = year_start_data['qty_visited_pensioners']
    ws['M6'] = year_start_data['qty_visited_invalids']
    ws['N6'] = year_start_data['qty_visited_out_station']
    ws['O6'] = year_start_data['qty_visited_online']
    ws['P6'] = year_start_data['note']

    # Записываем данные в строку 7 (текущий месяц)
    row_num = 7
    first_day, first_data = next(iter(sorted(daily_data.items())))
    ws[f'A{row_num}'] = first_day
    ws[f'B{row_num}'] = first_data['qty_reg_14'] + first_data['qty_reg_15_35'] + first_data['qty_reg_other']
    ws[f'C{row_num}'] = first_data['qty_reg_14']
    ws[f'D{row_num}'] = first_data['qty_reg_15_35']
    ws[f'E{row_num}'] = first_data['qty_reg_other']
    ws[f'F{row_num}'] = first_data['qty_reg_pensioners']
    ws[f'G{row_num}'] = first_data['qty_reg_invalid']
    ws[f'H{row_num}'] = first_data['qty_visited_14'] + first_data['qty_visited_15_35'] + first_data['qty_visited_other'] + first_data['qty_visited_online']
    ws[f'I{row_num}'] = first_data['qty_visited_14']
    ws[f'J{row_num}'] = first_data['qty_visited_15_35']
    ws[f'K{row_num}'] = first_data['qty_visited_other']
    ws[f'L{row_num}'] = first_data['qty_visited_pensioners']
    ws[f'M{row_num}'] = first_data['qty_visited_invalids']
    ws[f'N{row_num}'] = first_data['qty_visited_out_station']
    ws[f'O{row_num}'] = first_data['qty_visited_online']
    ws[f'P{row_num}'] = first_data['note']

    # Если данных больше, добавляем новые строки ниже строки 7
    if len(daily_data) > 1:
        for day, data in sorted(daily_data.items())[1:]:
            row_num += 1
            ws.insert_rows(row_num)  # Вставляем новую строку
            for col in range(1, ws.max_column + 1):
                ws.cell(row=row_num, column=col)._style = ws.cell(row=7, column=col)._style  # Копируем стили

            ws[f'A{row_num}'] = day
            ws[f'B{row_num}'] = data['qty_reg_14'] + data['qty_reg_15_35'] + data['qty_reg_other']
            ws[f'C{row_num}'] = data['qty_reg_14']
            ws[f'D{row_num}'] = data['qty_reg_15_35']
            ws[f'E{row_num}'] = data['qty_reg_other']
            ws[f'F{row_num}'] = data['qty_reg_pensioners']
            ws[f'G{row_num}'] = data['qty_reg_invalid']
            ws[f'H{row_num}'] = data['qty_visited_14'] + data['qty_visited_15_35'] + data['qty_visited_other'] + data['qty_visited_online']
            ws[f'I{row_num}'] = data['qty_visited_14']
            ws[f'J{row_num}'] = data['qty_visited_15_35']
            ws[f'K{row_num}'] = data['qty_visited_other']
            ws[f'L{row_num}'] = data['qty_visited_pensioners']
            ws[f'M{row_num}'] = data['qty_visited_invalids']
            ws[f'N{row_num}'] = data['qty_visited_out_station']
            ws[f'O{row_num}'] = data['qty_visited_online']
            ws[f'P{row_num}'] = data['note']

    # Сохраняем файл в HttpResponse
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=visit_reports.xlsx'
    wb.save(response)
    return response


def generate_book_report_excel(user, year, month):
    # Получаем сотрудника и филиал
    try:
        employee = Employee.objects.get(user=user)
        branch = employee.branch
    except Employee.DoesNotExist:
        return None

    if not branch:
        return None

    # Фильтруем отчеты по филиалу, году и месяцу (текущий месяц)
    book_reports_current_month = BookReport.objects.filter(
        library=branch,
        date__year=year,
        date__month=month
    ).order_by('date')

    # Фильтруем отчеты с начала года до текущего месяца (включая текущий месяц)
    book_reports_since_year_start = BookReport.objects.filter(
        library=branch,
        date__year=year,
        date__month__lte=month  # Все месяцы с начала года до текущего
    ).order_by('date')

    # Загружаем шаблон
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, 'reports/excell/books_template.xlsx')

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"File not found: {template_path}")

    wb = openpyxl.load_workbook(filename=template_path)
    ws = wb.active

    # Устанавливаем год в заголовке
    ws['A1'] = f"УЧЁТ ВЫДАЧИ ПЕЧАТНЫХ ИЗДАНИЙ, ИЗДАНИЙ НА ДРУГИХ НОСИТЕЛЯХ И СПРАВОЧНО-БИБЛИОГРАФИЧЕСКОЙ РАБОТЫ за {year} г."

    # Словарь для агрегации данных по дням (текущий месяц)
    daily_data = {}

    # Словарь для агрегации данных с начала года (включая текущий месяц)
    year_start_data = {
        'qty_books_14': 0,
        'qty_books_15_35': 0,
        'qty_books_other': 0,
        'qty_books_invalid': 0,
        'qty_books_neb': 0,
        'qty_books_prlib': 0,
        'qty_books_litres': 0,
        'qty_books_consultant': 0,
        'qty_books_local_library': 0,
        'qty_books_part_opl': 0,
        'qty_books_part_enm': 0,
        'qty_books_part_tech': 0,
        'qty_books_part_sh': 0,
        'qty_books_part_si': 0,
        'qty_books_part_yl': 0,
        'qty_books_part_hl': 0,
        'qty_books_part_dl': 0,
        'qty_books_part_other': 0,
        'qty_books_part_audio': 0,
        'qty_books_part_krai': 0,
        'qty_books_reference_do_14': 0,
        'qty_books_reference_14': 0,
        'qty_books_reference_35': 0,
        'qty_books_reference_other': 0,
        'qty_books_reference_invalid': 0,
        'qty_books_reference_online': 0,
        'note': ''
    }

    # Словарь для агрегации данных за текущий месяц
    current_month_data = {
        'qty_books_14': 0,
        'qty_books_15_35': 0,
        'qty_books_other': 0,
        'qty_books_invalid': 0,
        'qty_books_neb': 0,
        'qty_books_prlib': 0,
        'qty_books_litres': 0,
        'qty_books_consultant': 0,
        'qty_books_local_library': 0,
        'qty_books_part_opl': 0,
        'qty_books_part_enm': 0,
        'qty_books_part_tech': 0,
        'qty_books_part_sh': 0,
        'qty_books_part_si': 0,
        'qty_books_part_yl': 0,
        'qty_books_part_hl': 0,
        'qty_books_part_dl': 0,
        'qty_books_part_other': 0,
        'qty_books_part_audio': 0,
        'qty_books_part_krai': 0,
        'qty_books_reference_do_14': 0,
        'qty_books_reference_14': 0,
        'qty_books_reference_35': 0,
        'qty_books_reference_other': 0,
        'qty_books_reference_invalid': 0,
        'qty_books_reference_online': 0,
        'note': ''
    }

    # Агрегируем данные по дням (текущий месяц)
    for report in book_reports_current_month:
        date_key = report.date.day
        if date_key not in daily_data:
            daily_data[date_key] = {
                'qty_books_14': 0,
                'qty_books_15_35': 0,
                'qty_books_other': 0,
                'qty_books_invalid': 0,
                'qty_books_neb': 0,
                'qty_books_prlib': 0,
                'qty_books_litres': 0,
                'qty_books_consultant': 0,
                'qty_books_local_library': 0,
                'qty_books_part_opl': 0,
                'qty_books_part_enm': 0,
                'qty_books_part_tech': 0,
                'qty_books_part_sh': 0,
                'qty_books_part_si': 0,
                'qty_books_part_yl': 0,
                'qty_books_part_hl': 0,
                'qty_books_part_dl': 0,
                'qty_books_part_other': 0,
                'qty_books_part_audio': 0,
                'qty_books_part_krai': 0,
                'qty_books_reference_do_14': 0,
                'qty_books_reference_14': 0,
                'qty_books_reference_35': 0,
                'qty_books_reference_other': 0,
                'qty_books_reference_invalid': 0,
                'qty_books_reference_online': 0,
                'note': ''
            }
        daily_data[date_key]['qty_books_14'] += report.qty_books_14
        daily_data[date_key]['qty_books_15_35'] += report.qty_books_15_35
        daily_data[date_key]['qty_books_other'] += report.qty_books_other
        daily_data[date_key]['qty_books_invalid'] += report.qty_books_invalid
        daily_data[date_key]['qty_books_neb'] += report.qty_books_neb
        daily_data[date_key]['qty_books_prlib'] += report.qty_books_prlib
        daily_data[date_key]['qty_books_litres'] += report.qty_books_litres
        daily_data[date_key]['qty_books_consultant'] += report.qty_books_consultant
        daily_data[date_key]['qty_books_local_library'] += report.qty_books_local_library
        daily_data[date_key]['qty_books_part_opl'] += report.qty_books_part_opl
        daily_data[date_key]['qty_books_part_enm'] += report.qty_books_part_enm
        daily_data[date_key]['qty_books_part_tech'] += report.qty_books_part_tech
        daily_data[date_key]['qty_books_part_sh'] += report.qty_books_part_sh
        daily_data[date_key]['qty_books_part_si'] += report.qty_books_part_si
        daily_data[date_key]['qty_books_part_yl'] += report.qty_books_part_yl
        daily_data[date_key]['qty_books_part_hl'] += report.qty_books_part_hl
        daily_data[date_key]['qty_books_part_dl'] += report.qty_books_part_dl
        daily_data[date_key]['qty_books_part_other'] += report.qty_books_part_other
        daily_data[date_key]['qty_books_part_audio'] += report.qty_books_part_audio
        daily_data[date_key]['qty_books_part_krai'] += report.qty_books_part_krai
        daily_data[date_key]['qty_books_reference_do_14'] += report.qty_books_reference_do_14
        daily_data[date_key]['qty_books_reference_14'] += report.qty_books_reference_14
        daily_data[date_key]['qty_books_reference_35'] += report.qty_books_reference_35
        daily_data[date_key]['qty_books_reference_other'] += report.qty_books_reference_other
        daily_data[date_key]['qty_books_reference_invalid'] += report.qty_books_reference_invalid
        daily_data[date_key]['qty_books_reference_online'] += report.qty_books_reference_online
        daily_data[date_key]['note'] += report.note + " " if report.note else ""

        # Собираем данные за текущий месяц
        current_month_data['qty_books_14'] += report.qty_books_14
        current_month_data['qty_books_15_35'] += report.qty_books_15_35
        current_month_data['qty_books_other'] += report.qty_books_other
        current_month_data['qty_books_invalid'] += report.qty_books_invalid
        current_month_data['qty_books_neb'] += report.qty_books_neb
        current_month_data['qty_books_prlib'] += report.qty_books_prlib
        current_month_data['qty_books_litres'] += report.qty_books_litres
        current_month_data['qty_books_consultant'] += report.qty_books_consultant
        current_month_data['qty_books_local_library'] += report.qty_books_local_library
        current_month_data['qty_books_part_opl'] += report.qty_books_part_opl
        current_month_data['qty_books_part_enm'] += report.qty_books_part_enm
        current_month_data['qty_books_part_tech'] += report.qty_books_part_tech
        current_month_data['qty_books_part_sh'] += report.qty_books_part_sh
        current_month_data['qty_books_part_si'] += report.qty_books_part_si
        current_month_data['qty_books_part_yl'] += report.qty_books_part_yl
        current_month_data['qty_books_part_hl'] += report.qty_books_part_hl
        current_month_data['qty_books_part_dl'] += report.qty_books_part_dl
        current_month_data['qty_books_part_other'] += report.qty_books_part_other
        current_month_data['qty_books_part_audio'] += report.qty_books_part_audio
        current_month_data['qty_books_part_krai'] += report.qty_books_part_krai
        current_month_data['qty_books_reference_do_14'] += report.qty_books_reference_do_14
        current_month_data['qty_books_reference_14'] += report.qty_books_reference_14
        current_month_data['qty_books_reference_35'] += report.qty_books_reference_35
        current_month_data['qty_books_reference_other'] += report.qty_books_reference_other
        current_month_data['qty_books_reference_invalid'] += report.qty_books_reference_invalid
        current_month_data['qty_books_reference_online'] += report.qty_books_reference_online
        current_month_data['note'] += report.note + " " if report.note else ""

    # Агрегируем данные с начала года (включая текущий месяц)
    for report in book_reports_since_year_start:
        year_start_data['qty_books_14'] += report.qty_books_14
        year_start_data['qty_books_15_35'] += report.qty_books_15_35
        year_start_data['qty_books_other'] += report.qty_books_other
        year_start_data['qty_books_invalid'] += report.qty_books_invalid
        year_start_data['qty_books_neb'] += report.qty_books_neb
        year_start_data['qty_books_prlib'] += report.qty_books_prlib
        year_start_data['qty_books_litres'] += report.qty_books_litres
        year_start_data['qty_books_consultant'] += report.qty_books_consultant
        year_start_data['qty_books_local_library'] += report.qty_books_local_library
        year_start_data['qty_books_part_opl'] += report.qty_books_part_opl
        year_start_data['qty_books_part_enm'] += report.qty_books_part_enm
        year_start_data['qty_books_part_tech'] += report.qty_books_part_tech
        year_start_data['qty_books_part_sh'] += report.qty_books_part_sh
        year_start_data['qty_books_part_si'] += report.qty_books_part_si
        year_start_data['qty_books_part_yl'] += report.qty_books_part_yl
        year_start_data['qty_books_part_hl'] += report.qty_books_part_hl
        year_start_data['qty_books_part_dl'] += report.qty_books_part_dl
        year_start_data['qty_books_part_other'] += report.qty_books_part_other
        year_start_data['qty_books_part_audio'] += report.qty_books_part_audio
        year_start_data['qty_books_part_krai'] += report.qty_books_part_krai
        year_start_data['qty_books_reference_do_14'] += report.qty_books_reference_do_14
        year_start_data['qty_books_reference_14'] += report.qty_books_reference_14
        year_start_data['qty_books_reference_35'] += report.qty_books_reference_35
        year_start_data['qty_books_reference_other'] += report.qty_books_reference_other
        year_start_data['qty_books_reference_invalid'] += report.qty_books_reference_invalid
        year_start_data['qty_books_reference_online'] += report.qty_books_reference_online
        year_start_data['note'] += report.note + " " if report.note else ""

    # Вычитаем данные за текущий месяц из итогов с начала года
    for key in year_start_data:
        if key != 'note':  # Примечания не суммируются
            year_start_data[key] -= current_month_data[key]

    # Записываем данные с начала года (без текущего месяца) в строку 6
    ws['B5'] = year_start_data['qty_books_14'] + year_start_data['qty_books_15_35'] + year_start_data['qty_books_other']
    ws['C5'] = year_start_data['qty_books_14']
    ws['D5'] = year_start_data['qty_books_15_35']
    ws['E5'] = year_start_data['qty_books_invalid']
    ws['F5'] = year_start_data['qty_books_neb']
    ws['G5'] = year_start_data['qty_books_prlib']
    ws['H5'] = year_start_data['qty_books_litres']
    ws['I5'] = year_start_data['qty_books_consultant']
    ws['K5'] = year_start_data['qty_books_local_library']
    ws['L5'] = year_start_data['qty_books_part_opl'] + year_start_data['qty_books_part_enm'] + year_start_data['qty_books_part_tech']
    + year_start_data['qty_books_part_sh'] + year_start_data['qty_books_part_si'] + year_start_data['qty_books_part_yl']
    + year_start_data['qty_books_part_hl'] + year_start_data['qty_books_part_hl'] + year_start_data['qty_books_part_dl']
    + year_start_data['qty_books_part_other'] + year_start_data['qty_books_part_audio'] + year_start_data['qty_books_part_krai']
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
    ws['X5'] = year_start_data['qty_books_reference_do_14'] + year_start_data['qty_books_reference_35'] + year_start_data['qty_books_reference_other']
    ws['Y5'] = year_start_data['qty_books_reference_do_14']
    ws['Z5'] = year_start_data['qty_books_reference_14']
    ws['AA5'] = year_start_data['qty_books_reference_35']
    ws['AB5'] = year_start_data['qty_books_reference_invalid']
    ws['AC5'] = year_start_data['qty_books_reference_online']
    ws['AD5'] = year_start_data['note']

    # Записываем данные в строку 7 (текущий месяц)
    row_num = 6
    first_day, first_data = next(iter(sorted(daily_data.items())))
    ws[f'A{row_num}'] = first_day
    ws[f'B{row_num}'] = first_data['qty_books_14'] + first_data['qty_books_15_35'] + first_data['qty_books_other']
    ws[f'C{row_num}'] = first_data['qty_books_14']
    ws[f'D{row_num}'] = first_data['qty_books_15_35']
    ws[f'E{row_num}'] = first_data['qty_books_other']
    ws[f'F{row_num}'] = first_data['qty_books_invalid']
    ws[f'G{row_num}'] = first_data['qty_books_neb']
    ws[f'H{row_num}'] = first_data['qty_books_prlib']
    ws[f'I{row_num}'] = first_data['qty_books_litres']
    ws[f'J{row_num}'] = first_data['qty_books_consultant']
    ws[f'K{row_num}'] = first_data['qty_books_local_library']
    ws[f'L{row_num}'] = first_data['qty_books_part_opl'] + first_data['qty_books_part_enm'] + first_data['qty_books_part_tech']
    + first_data['qty_books_part_sh'] + first_data['qty_books_part_si'] + first_data['qty_books_part_yl'] + first_data['qty_books_part_hl']
    + first_data['qty_books_part_dl'] + first_data['qty_books_part_other'] + first_data['qty_books_part_audio'] + first_data['qty_books_part_krai']
    ws[f'M{row_num}'] = first_data['qty_books_part_opl']
    ws[f'N{row_num}'] = first_data['qty_books_part_enm']
    ws[f'O{row_num}'] = first_data['qty_books_part_tech']
    ws[f'P{row_num}'] = first_data['qty_books_part_sh']
    ws[f'Q{row_num}'] = first_data['qty_books_part_si']
    ws[f'R{row_num}'] = first_data['qty_books_part_yl']
    ws[f'S{row_num}'] = first_data['qty_books_part_hl']
    ws[f'T{row_num}'] = first_data['qty_books_part_dl']
    ws[f'U{row_num}'] = first_data['qty_books_part_other']
    ws[f'V{row_num}'] = first_data['qty_books_part_audio']
    ws[f'W{row_num}'] = first_data['qty_books_part_krai']
    ws[f'X{row_num}'] = first_data['qty_books_reference_do_14'] + first_data['qty_books_reference_14'] + first_data['qty_books_reference_35']
    ws[f'Y{row_num}'] = first_data['qty_books_reference_do_14']
    ws[f'Z{row_num}'] = first_data['qty_books_reference_14']
    ws[f'AA{row_num}'] = first_data['qty_books_reference_35']
    ws[f'AB{row_num}'] = first_data['qty_books_reference_invalid']
    ws[f'AC{row_num}'] = first_data['qty_books_reference_online']
    ws[f'AD{row_num}'] = first_data['note']

    # Если данных больше, добавляем новые строки ниже строки 6
    if len(daily_data) > 1:
        for day, data in sorted(daily_data.items())[1:]:
            row_num += 1
            ws.insert_rows(row_num)  # Вставляем новую строку
            for col in range(1, ws.max_column + 1):
                ws.cell(row=row_num, column=col)._style = ws.cell(row=6, column=col)._style  # Копируем стили

            ws[f'A{row_num}'] = day
            ws[f'B{row_num}'] = data['qty_books_14'] + data['qty_books_15_35'] + data['qty_books_other']
            ws[f'C{row_num}'] = data['qty_books_14']
            ws[f'D{row_num}'] = data['qty_books_15_35']
            ws[f'E{row_num}'] = data['qty_books_other']
            ws[f'F{row_num}'] = data['qty_books_invalid']
            ws[f'G{row_num}'] = data['qty_books_neb']
            ws[f'H{row_num}'] = data['qty_books_prlib']
            ws[f'I{row_num}'] = data['qty_books_litres']
            ws[f'J{row_num}'] = data['qty_books_consultant']
            ws[f'K{row_num}'] = data['qty_books_local_library']
            ws[f'L{row_num}'] = data['qty_books_part_opl'] + data['qty_books_part_enm'] + data['qty_books_part_tech']
            + data['qty_books_part_sh'] + data['qty_books_part_si'] + data['qty_books_part_yl'] + data['qty_books_part_hl']
            + data['qty_books_part_dl'] + data['qty_books_part_other'] + data['qty_books_part_audio'] + data['qty_books_part_krai']
            ws[f'M{row_num}'] = data['qty_books_part_opl']
            ws[f'N{row_num}'] = data['qty_books_part_enm']
            ws[f'O{row_num}'] = data['qty_books_part_tech']
            ws[f'P{row_num}'] = data['qty_books_part_sh']
            ws[f'Q{row_num}'] = data['qty_books_part_si']
            ws[f'R{row_num}'] = data['qty_books_part_yl']
            ws[f'S{row_num}'] = data['qty_books_part_hl']
            ws[f'T{row_num}'] = data['qty_books_part_dl']
            ws[f'U{row_num}'] = data['qty_books_part_other']
            ws[f'V{row_num}'] = data['qty_books_part_audio']
            ws[f'W{row_num}'] = data['qty_books_part_krai']
            ws[f'X{row_num}'] = data['qty_books_reference_do_14'] + data['qty_books_reference_14'] + \
                                data['qty_books_reference_35']
            ws[f'Y{row_num}'] = data['qty_books_reference_do_14']
            ws[f'Z{row_num}'] = data['qty_books_reference_14']
            ws[f'AA{row_num}'] = data['qty_books_reference_35']
            ws[f'AB{row_num}'] = data['qty_books_reference_invalid']
            ws[f'AC{row_num}'] = data['qty_books_reference_online']
            ws[f'AD{row_num}'] = data['note']

    # Сохраняем файл в HttpResponse
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=book_reports.xlsx'
    wb.save(response)
    return response