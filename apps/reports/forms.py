from django import forms
from .models import Event
from ..core.models import Employee, Cafedra


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['cafedra', 'name', 'date', 'direction',
                  'quantity', 'as_part', 'age_14',
                  'age_35', 'age_other',
                  'invalids', 'out_of_station', 'as_part', 'paid', 'note']
        widgets = {
            'cafedra': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={
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
            'paid': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            employee = Employee.objects.get(user=user)
            self.fields['cafedra'].queryset = Cafedra.objects.filter(library=employee.branch)