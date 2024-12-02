from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'library',
            'name',
            'date',
            'direction',
            'quantity',
            'age_group',
            'age_14',
            'age_35',
            'age_54',
            'age_other',
            'invalids',
            'out_of_station',
            'note',
        ]
        # Optionally, you can specify widgets for specific fields
        # For example:
        # widgets = {
        #     'note': forms.Textarea(attrs={'rows': 4}),
        # }