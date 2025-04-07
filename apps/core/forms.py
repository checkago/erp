from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
        fields = '__all__'  # Включаем все поля модели
        widgets = {
            # Основная информация
            'organization': forms.Select(attrs={'class': 'form-select border border-1 border-dark'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'manager': forms.Select(attrs={'class': 'form-select border border-1 border-dark'}),
            'address': forms.TextInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'mail_address': forms.TextInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'phone': forms.TextInput(attrs={'class': 'form-control border border-1 border-dark'}),

            # Флаговые поля (чекбоксы)
            'department': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'adult': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'child': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'child_young': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'village': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'mod_lib': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),

            # Материально-техническая база (флаги)
            'object_federal_importance': forms.CheckboxInput(attrs={'class': 'btn-check', 'type': 'checkbox'}),
            'object_regional_importance': forms.CheckboxInput(attrs={'class': 'btn-check', 'type': 'checkbox'}),
            'room_for_vision_disabled': forms.CheckboxInput(attrs={'class': 'btn-check', 'type': 'checkbox'}),
            'room_for_hearing_disabled': forms.CheckboxInput(attrs={'class': 'btn-check', 'type': 'checkbox'}),
            'room_for_musculoskeletal_system_disabled': forms.CheckboxInput(
                attrs={'class': 'btn-check', 'type': 'checkbox'}),

            # Числовые поля
            'area_full': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'area_fund': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'area_work': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'area_operation': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'area_rental': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'area_other': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'area_repair': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'area_emergency': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'out_of_station_service_points': forms.NumberInput(
                attrs={'class': 'form-control border border-1 border-dark'}),
            'seatings': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'seatings_computer': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'seatings_internet': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),

            # Автоматизированные технологии
            'autotech_electronic_catalog': forms.CheckboxInput(
                attrs={'class': 'btn-check'}),
            'autotech_funds_disbursement': forms.CheckboxInput(
                attrs={'class': 'btn-check'}),
            'autotech_user_access': forms.CheckboxInput(attrs={'class': 'btn-check'}),
            'autotech_funds_documents': forms.CheckboxInput(attrs={'class': 'btn-check'}),
            'autotech_funds_digitization': forms.CheckboxInput(
                attrs={'class': 'btn-check'}),

            # Оборудование и транспорт
            'invalids_equipment': forms.CheckboxInput(attrs={'class': 'btn-check'}),
            'cars': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),
            'cars_special': forms.NumberInput(attrs={'class': 'form-control border border-1 border-dark'}),

            # Интернет и ресурсы
            'availability_internet': forms.CheckboxInput(attrs={'class': 'btn-check'}),
            'availability_internet_for_users': forms.CheckboxInput(
                attrs={'class': 'btn-check'}),
            'availability_site': forms.CheckboxInput(attrs={'class': 'btn-check'}),
            'availability_site_for_disabled': forms.CheckboxInput(
                attrs={'class': 'btn-check'}),
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


