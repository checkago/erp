from django import forms
from .models import ErpUser, Employee


class ErpUserForm(forms.ModelForm):
    class Meta:
        model = ErpUser
        fields = ('first_name', 'last_name', 'email', 'avatar', 'bio')


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('position', 'branch', 'phone', 'start_date', 'end_date')
