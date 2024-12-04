from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['cafedra', 'name', 'date', 'direction',
                  'quantity', 'as_part', 'age_14',
                  'age_35', 'age_other',
                  'invalids', 'out_of_station', 'note']
        widgets = {
            'cafedra': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={
                'class': 'datepicker-here form-control digits',
                'type': 'date',
                'data-date-format': 'mm.dd.yyyy'
            }),
            'direction': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'age_14': forms.TextInput(attrs={'class': 'form-control'}),
            'age_35': forms.TextInput(attrs={'class': 'form-control'}),
            'age_other': forms.TextInput(attrs={'class': 'form-control'}),
            'invalids': forms.TextInput(attrs={'class': 'form-control'}),
            'out_of_station': forms.TextInput(attrs={'class': 'form-control'}),
            'as_part': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)