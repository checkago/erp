from django import forms
from .models import Event, ChildBookReport, AdultBookReport, AdultVisitReport, ChildVisitReport
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


class AdultBookReportForm(forms.ModelForm):
    class Meta:
        model = AdultBookReport
        fields = ['cafedra', 'date', 'qty_books_14', 'qty_books_35', 'qty_books_invalid',
                  'qty_books_part_opl', 'qty_books_part_enm', 'qty_books_part_tech',
                  'qty_books_part_sh', 'qty_books_part_si', 'qty_books_part_yl',
                  'qty_books_part_hl', 'qty_books_part_dl', 'qty_books_part_other',
                  'qty_books_part_audio', 'qty_books_part_krai', 'qty_books_reference_14',
                  'qty_books_reference_35', 'qty_books_reference_invalid', 'qty_books_reference_online',
                  'note']
        widgets = {
            'cafedra': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={
                'class': 'datepicker-here form-control digits',
                'data-date-format': 'mm.dd.yyyy'
            }),
            'qty_books_14': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_35': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_invalid': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_opl': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_enm': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_tech': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_sh': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_si': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_yl': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_hl': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_dl': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_audio': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_krai': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_reference_14': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_reference_35': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_reference_invalid': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_reference_online': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            employee = Employee.objects.get(user=user)
            self.fields['cafedra'].queryset = Cafedra.objects.filter(library=employee.branch)
            self.initial['library'] = employee.branch
            self.fields['library'].widget.attrs['disabled'] = True
            self.fields['library'].widget.attrs['readonly'] = True


class AdultVisitReportForm(forms.ModelForm):
    class Meta:
        model = AdultVisitReport
        fields = ['cafedra', 'date', 'qty_reg_35', 'qty_reg_other', 'qty_reg_invalid',
                  'qty_visited_35', 'qty_visited_other', 'qty_visited_invalids',
                  'qty_events_35', 'qty_events_other', 'qty_events_invalids',
                  'qty_events_out_station', 'qty_online_requests', 'qty_paid', 'note']
        widgets = {
            'cafedra': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.TextInput(attrs={
                'class': 'datepicker-here form-control digits',
                'type': 'date',
                'data-date-format': 'mm.dd.yyyy'
            }),
            'qty_reg_35': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_reg_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_reg_invalid': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_visited_35': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_visited_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_visited_invalids': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_events_35': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_events_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_events_invalids': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_events_out_station': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_online_requests': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            employee = Employee.objects.get(user=user)
            self.fields['cafedra'].queryset = Cafedra.objects.filter(library=employee.branch)
            self.initial['library'] = employee.branch
            self.fields['library'].widget.attrs['disabled'] = True
            self.fields['library'].widget.attrs['readonly'] = True


class ChildVisitReportForm(forms.ModelForm):
    class Meta:
        model = ChildVisitReport
        fields = ['cafedra', 'date', 'qty_reg_7', 'qty_reg_14', 'qty_reg_30', 'qty_reg_other',
                  'qty_visited_14', 'qty_visited_35', 'qty_visited_other', 'qty_visited_invalids',
                  'qty_visited_out_station', 'qty_events_14', 'qty_events_35', 'qty_events_other',
                  'qty_events_invalids', 'qty_events_out_station', 'qty_online_requests', 'qty_paid', 'note']
        widgets = {
            'cafedra': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.TextInput(attrs={
                'class': 'datepicker-here form-control digits',
                'type': 'date',
                'data-date-format': 'mm.dd.yyyy'
            }),
            'qty_reg_7': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_reg_14': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_reg_30': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_reg_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_visited_14': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_visited_35': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_visited_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_visited_invalids': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_visited_out_station': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_events_14': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_events_35': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_events_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_events_invalids': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_events_out_station': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_online_requests': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            employee = Employee.objects.get(user=user)
            self.fields['cafedra'].queryset = Cafedra.objects.filter(library=employee.branch)


class AdultBookReportForm(forms.ModelForm):
    class Meta:
        model = AdultBookReport
        fields = ['cafedra', 'date', 'qty_books_14', 'qty_books_35', 'qty_books_invalid',
                  'qty_books_part_opl', 'qty_books_part_enm', 'qty_books_part_tech',
                  'qty_books_part_sh', 'qty_books_part_si', 'qty_books_part_yl',
                  'qty_books_part_hl', 'qty_books_part_dl', 'qty_books_part_other',
                  'qty_books_part_audio', 'qty_books_part_krai', 'qty_books_reference_14',
                  'qty_books_reference_35', 'qty_books_reference_invalid', 'qty_books_reference_online',
                  'note']
        widgets = {
            'cafedra': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.TextInput(attrs={
                'class': 'datepicker-here form-control digits',
                'type': 'date',
                'data-date-format': 'mm.dd.yyyy'
            }),
            'qty_books_14': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_35': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_invalid': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_opl': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_enm': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_tech': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_sh': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_si': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_yl': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_hl': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_dl': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_audio': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_krai': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_reference_14': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_reference_35': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_reference_invalid': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_reference_online': forms.NumberInput(attrs={'class': 'form-control'}),
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
        fields = ['cafedra', 'date', 'qty_books_14', 'qty_books_30', 'qty_books_other',
                  'qty_books_part_opl', 'qty_books_part_enm', 'qty_books_part_tech',
                  'qty_books_part_sh', 'qty_books_part_si', 'qty_books_part_yl',
                  'qty_books_part_hl', 'qty_books_part_dl', 'qty_books_part_other',
                  'qty_books_part_audio', 'qty_books_part_krai', 'qty_books_reference_14',
                  'qty_books_reference_30', 'qty_books_reference_other', 'qty_books_reference_online',
                  'note']
        widgets = {
            'cafedra': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.TextInput(attrs={
                'class': 'datepicker-here form-control digits',
                'type': 'date',
                'data-date-format': 'mm.dd.yyyy'
            }),
            'qty_books_14': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_30': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_opl': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_enm': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_tech': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_sh': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_si': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_yl': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_hl': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_dl': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_audio': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_part_krai': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_reference_14': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_reference_30': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_reference_other': forms.NumberInput(attrs={'class': 'form-control'}),
            'qty_books_reference_online': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            employee = Employee.objects.get(user=user)
            self.fields['cafedra'].queryset = Cafedra.objects.filter(library=employee.branch)