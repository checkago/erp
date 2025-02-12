import os
import openpyxl
from django.http import HttpResponse
from .models import VisitReport
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

    # Фильтруем отчеты по филиалу, году и месяцу
    visit_reports = VisitReport.objects.filter(
        library=branch,
        date__year=year,
        date__month=month
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

    # Словарь для агрегации данных по дням
    daily_data = {}

    # Агрегируем данные по дням
    for report in visit_reports:
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

    # Рассчитываем итоговые значения
    total_reg_14 = sum(data['qty_reg_14'] for data in daily_data.values())
    total_reg_15_35 = sum(data['qty_reg_15_35'] for data in daily_data.values())
    total_reg_other = sum(data['qty_reg_other'] for data in daily_data.values())
    total_reg_pensioners = sum(data['qty_reg_pensioners'] for data in daily_data.values())
    total_reg_invalid = sum(data['qty_reg_invalid'] for data in daily_data.values())
    total_visited_14 = sum(data['qty_visited_14'] for data in daily_data.values())
    total_visited_15_35 = sum(data['qty_visited_15_35'] for data in daily_data.values())
    total_visited_other = sum(data['qty_visited_other'] for data in daily_data.values())
    total_visited_pensioners = sum(data['qty_visited_pensioners'] for data in daily_data.values())
    total_visited_invalids = sum(data['qty_visited_invalids'] for data in daily_data.values())
    total_visited_out_station = sum(data['qty_visited_out_station'] for data in daily_data.values())
    total_visited_online = sum(data['qty_visited_online'] for data in daily_data.values())

    # Записываем данные в строку 7
    row_num = 7
    first_day, first_data = next(iter(sorted(daily_data.items())))
    ws[f'A{row_num}'] = first_day
    ws[f'B{row_num}'] = first_data['qty_reg_14'] + first_data['qty_reg_15_35'] + first_data['qty_reg_other']  # Сумма C, D, E
    ws[f'C{row_num}'] = first_data['qty_reg_14']
    ws[f'D{row_num}'] = first_data['qty_reg_15_35']
    ws[f'E{row_num}'] = first_data['qty_reg_other']
    ws[f'F{row_num}'] = first_data['qty_reg_pensioners']
    ws[f'G{row_num}'] = first_data['qty_reg_invalid']
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