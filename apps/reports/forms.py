from django import forms
from .models import Event, ChildBookReport
from ..core.models import Employee, Cafedra


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['cafedra', 'name', 'date', 'direction',
                  'quantity', 'as_part', 'age_14',
                  'age_35', 'age_other', 'invalids', 'out_of_station', 'as_part', 'paid', 'note']
        widgets = {
            'cafedra': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={
                'class': 'datepicker-here form-control digits',
                'type': 'date',
                'data-date-format': 'mm.dd.yyyy'
            }),
            'direction': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'age_14': forms.NumberInput(attrs={'class': 'form-control'}),
            'age_35': forms.NumberInput(attrs={'class': 'form-control'}),
            'age_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'invalids': forms.NumberInput(attrs={'class': 'form-control'}),
            'out_of_station': forms.NumberInput(attrs={'class': 'form-control'}),
            'as_part': forms.Select(attrs={'class': 'form-select'}),
            'paid': forms.CheckboxInput(attrs={'class': 'form-check-input pt-2'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            employee = Employee.objects.get(user=user)
            self.fields['cafedra'].queryset = Cafedra.objects.filter(library=employee.branch)


class ChildBookReportForm(forms.ModelForm):
    class Meta:
        model = ChildBookReport
        fields = [
            'cafedra', 'date', 'qty_books_14', 'qty_books_30',
            'qty_books_other', 'qty_books_part_opl',
            'qty_books_part_enm', 'qty_books_part_tech',
            'qty_books_part_sh', 'qty_books_part_si',
            'qty_books_part_yl', 'qty_books_part_hl',
            'qty_books_part_dl', 'qty_books_part_other',
            'qty_books_part_audio', 'qty_books_part_krai',
            'qty_books_reference_14', 'qty_books_reference_30',
            'qty_books_reference_other', 'qty_books_reference_online',
            'note'
        ]
        widgets = {
            'cafedra': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # Добавьте остальные поля с соответствующими виджетами
            'note': forms.Textarea(attrs={'class': 'form-control'}),
        }