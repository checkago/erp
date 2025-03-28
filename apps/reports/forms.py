from django import forms
from .models import Event, BookReport, VisitReport
from apps.core.models import Employee, Cafedra


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['cafedra', 'name', 'date', 'direction',
                  'quantity', 'as_part', 'age_14',
                  'age_35', 'age_other', 'invalids', 'pensioners', 'out_of_station', 'as_part', 'paid', 'note']
        widgets = {
            'cafedra': forms.Select(attrs={'class': 'form-select border border-1 border-dark'}),
            'name': forms.TextInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'date': forms.TextInput(attrs={
                'class': 'datepicker-here form-control digits border border-1 border-dark',
                'type': 'date',
                'data-date-format': 'mm.dd.yyyy'
            }),
            'direction': forms.Select(attrs={'class': 'form-select border border-1 border-dark'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'age_14': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'age_35': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'age_other': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'invalids': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'pensioners': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'out_of_station': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'as_part': forms.Select(attrs={'class': 'form-select border border-1 border-dark'}),
            'paid': forms.CheckboxInput(attrs={
                'class': 'btn-check',
                'type': 'checkbox',
                'id': 'paid',
                'autocomplete': 'off'
            }),
            'note': forms.Textarea(attrs={'class': 'form-control border border-1 border-dark', 'rows': '1'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            employee = Employee.objects.get(user=user)
            self.fields['cafedra'].queryset = Cafedra.objects.filter(library=employee.branch)


class BookReportForm(forms.ModelForm):
    class Meta:
        model = BookReport
        fields = ['cafedra', 'date', 'qty_books_14', 'qty_books_15_35', 'qty_books_other', 'qty_books_invalid', 'qty_books_out_of_station',
                  'qty_books_neb', 'qty_books_prlib', 'qty_books_litres', 'qty_books_consultant',
                  'qty_books_local_library', 'qty_books_part_opl', 'qty_books_part_enm', 'qty_books_part_tech',
                  'qty_books_part_sh', 'qty_books_part_si', 'qty_books_part_yl', 'qty_books_part_hl', 'qty_books_part_dl',
                  'qty_books_part_other', 'qty_books_part_audio', 'qty_books_part_krai', 'qty_books_reference_do_14',
                  'qty_books_reference_14', 'qty_books_reference_35', 'qty_books_reference_invalid',
                  'qty_books_reference_online', 'note']
        widgets = {
            'cafedra': forms.Select(attrs={'class': 'form-select border border-1 border-dark'}),
            'date': forms.TextInput(attrs={
                'class': 'datepicker-here form-control digits border border-1 border-dark',
                'type': 'date',
                'data-date-format': 'mm.dd.yyyy'
            }),
            'qty_books_14': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_15_35': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_other': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_invalid': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_out_of_station': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_neb': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_prlib': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_litres': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_consultant': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_local_library': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_part_opl': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_part_enm': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_part_tech': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_part_sh': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_part_si': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_part_yl': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_part_hl': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_part_dl': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_part_other': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_part_audio': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_part_krai': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_reference_do_14': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_reference_14': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_reference_35': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_reference_invalid': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'qty_books_reference_online': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'note': forms.Textarea(attrs={'class': 'form-control border border-1 border-dark', 'rows': '1'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        mod_lib = kwargs.pop('mod_lib', False)  # Получаем статус модельной библиотеки
        super().__init__(*args, **kwargs)

        if user:
            employee = Employee.objects.get(user=user)
            self.fields['cafedra'].queryset = Cafedra.objects.filter(library=employee.branch)

            # Скрываем поля, если библиотека не модельная
            if not mod_lib:
                fields_to_hide = [
                    'qty_books_part_opl', 'qty_books_part_enm',
                    'qty_books_part_tech', 'qty_books_part_sh',
                    'qty_books_part_si', 'qty_books_part_yl',
                    'qty_books_part_hl', 'qty_books_part_dl',
                    'qty_books_part_other', 'qty_books_part_audio',
                    'qty_books_part_krai'
                ]
                for field in fields_to_hide:
                    self.fields[field].widget = forms.HiddenInput()  #


class VisitReportForm(forms.ModelForm):
    class Meta:
        model = VisitReport
        fields = ['cafedra', 'date', 'qty_reg_14', 'qty_reg_15_35', 'qty_reg_other', 'qty_reg_invalid', 'qty_reg_out_of_station', 'qty_reg_pensioners',
                  'qty_reg_prlib', 'qty_reg_litres', 'qty_visited_14', 'qty_visited_15_35', 'qty_visited_other',
                  'qty_visited_invalids', 'qty_visited_pensioners', 'qty_visited_prlib', 'qty_visited_litres', 'qty_visited_out_station',
                  'qty_visited_online', 'note']
        widgets = {
            'cafedra': forms.Select(attrs={'class': 'form-select border border-1 border-dark border border-1 border-dark'}),
            'date': forms.TextInput(attrs={
                'class': 'datepicker-here form-control digits border border-1 border-dark border border-1 border-dark',
                'type': 'date',
                'data-date-format': 'mm.dd.yyyy'
            }),
            'qty_reg_14': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_reg_15_35': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_reg_other': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_reg_invalid': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_reg_out_of_station': forms.NumberInput(
                attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_reg_pensioners': forms.NumberInput(
                attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_reg_prlib': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_reg_litres': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_visited_14': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_visited_15_35': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_visited_other': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_visited_invalids': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_visited_pensioners': forms.NumberInput(
                attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_visited_prlib': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_visited_litres': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_visited_out_station': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'qty_visited_online': forms.NumberInput(
                attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark'}),
            'note': forms.Textarea(attrs={'class': 'form-control border border-1 border-dark border border-1 border-dark', 'rows': '1'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            employee = Employee.objects.get(user=user)
            self.fields['cafedra'].queryset = Cafedra.objects.filter(library=employee.branch)
