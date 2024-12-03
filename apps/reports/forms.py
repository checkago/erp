from django import forms
from .models import Event
from ..core.models import Cafedra


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['cafedra', 'name', 'date', 'direction', 'quantity', 'age_group', 'age_14', 'age_35', 'age_54',
                  'age_other', 'invalids', 'out_of_station', 'note']

    def __init__(self, *args, **kwargs):
        branch = kwargs.pop('branch', None)
        super().__init__(*args, **kwargs)
        if branch:
            self.fields['cafedra'].queryset = Cafedra.objects.filter(library=branch)