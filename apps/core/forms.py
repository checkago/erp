from django import forms
from .models import ErpUser, Employee, Branch, Cafedra


class ErpUserForm(forms.ModelForm):
    class Meta:
        model = ErpUser
        fields = ('last_name', 'first_name', 'middle_name', 'email', 'avatar', 'bio')

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('phone',)


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ('full_name', 'short_name', 'manager', 'address', 'mail_address', 'email', 'phone', 'department',
                  'adult', 'child', 'mod_lib')

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'manager': forms.Select(attrs={'class': 'form-select border border-1 border-dark'}),
            'address': forms.TextInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'mail_address': forms.TextInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'email': forms.TextInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'phone': forms.TextInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'department': forms.CheckboxInput(attrs={
                'class': 'btn-check',
                'type': 'checkbox',
                'id': 'department'}),
            'adult': forms.CheckboxInput(attrs={
                'class': 'btn-check',
                'type': 'checkbox',
                'id': 'adult'}),
            'child': forms.CheckboxInput(attrs={
                'class': 'btn-check',
                'type': 'checkbox',
                'id': 'child'}),
            'mod_lib': forms.CheckboxInput(attrs={
                'class': 'btn-check',
                'type': 'checkbox',
                'id': 'mod_lib'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            employee = Employee.objects.get(user=user)
            self.fields['cafedra'].queryset = Cafedra.objects.filter(library=employee.branch)


class CafedraForm(forms.ModelForm):
    class Meta:
        model = Cafedra
        fields = ('name',)


