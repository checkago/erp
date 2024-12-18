from django import forms
from .models import ErpUser, Employee, Cafedra


class ErpUserForm(forms.ModelForm):
    class Meta:
        model = ErpUser
        fields = ('first_name', 'last_name', 'email', 'avatar', 'bio')

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('phone',)


class CafedraForm(forms.ModelForm):
    class Meta:
        model = Cafedra
        fields = ('name',)


