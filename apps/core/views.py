from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import generics

from apps.core.forms import ErpUserForm, EmployeeForm, BranchForm, CafedraForm
from apps.core.models import Employee, Branch, Position, Cafedra
from apps.core.serializers import EmployeeSerializer
from apps.reports.utils import get_totals, get_event_totals, get_book_totals


@login_required(login_url="/login_home")
# @cache_page(60 * 5)
def index(request):
    user = request.user
    totals_visits_branch = get_totals(user)
    totals_books_branch = get_book_totals(user)
    totals_event_branch = get_event_totals(user)
    context = {"breadcrumb": {"parent": "Главная", "child": "Рабочий стол"}, "jsFunction": 'startTime()',
               'totals_visits_branch': totals_visits_branch, 'totals_books_branch': totals_books_branch,
               'totals_event_branch': totals_event_branch}
    return render(request, "general/dashboard/index.html", context)


def login_home(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    nextPage = request.GET['next']
                    return HttpResponseRedirect(nextPage)
                return redirect("index")
            else:
                messages.error(request, "Wrong credentials")
                return redirect("login_home")
        else:
            messages.error(request, "Wrong credentials")
            return redirect("login_home")

    else:
        form = AuthenticationForm()

    return render(request, 'main-login.html', {"form": form, })


def logout_view(request):
    logout(request)
    return redirect('login_home')


def signup_home(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(email=email).exists()
        if user:
            raise Exception('Something went wrong')
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        return redirect('index')


@login_required(login_url="/login_home")
# @cache_page(60 * 5)
def employee_list_view(request):
    employees = Employee.objects.all()
    context = {"breadcrumb": {"parent": "Главная", "child": "Сотрудники"}, 'employees': employees}
    return render(request, 'employee_list.html', context=context)


class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


@login_required(login_url="/login_home")
# @cache_page(60 * 5)
def branch_list_view(request):
    branches = Branch.objects.all().order_by('short_name')
    context = {"breadcrumb": {"parent": "Главная", "child": "Филиалы"}, 'branches': branches}
    return render(request, 'branch_list.html', context=context)


@login_required
def branch_detail_view(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    employees = Employee.objects.filter(branch=branch).exclude(pk=branch.manager_id)
    if request.method == 'POST':
        form = CafedraForm(request.POST)
        if form.is_valid():
            cafedra = form.save(commit=False)
            cafedra.library = branch
            cafedra.save()
            return redirect('branch_detail', pk=pk)
    else:
        form = CafedraForm()
    context = {"breadcrumb": {"parent": "Филиалы", "child": branch.short_name}, 'branch': branch,
               'employees': employees, 'add_cafedra_form': form}
    return render(request, 'branch_detail.html', context=context)

@login_required
@permission_required('branch.change_branch', raise_exception=True)
def branch_edit_view(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    employee = request.user.employee
    if employee and employee.branch == branch:
        if request.method == 'POST':
            if 'add_cafedra_form' in request.POST:
                form = CafedraForm(request.POST)
                if form.is_valid():
                    cafedra = form.save(commit=False)
                    cafedra.library = branch
                    cafedra.save()
                    return redirect('branch_edit', pk=pk)
            else:
                form = BranchForm(request.POST, instance=branch)
                if form.is_valid():
                    form.save()
                    return redirect('branch_detail', pk=pk)
        else:
            form = BranchForm(instance=branch)
            add_cafedra_form = CafedraForm()
        context = {"breadcrumb": {"parent": "Филиалы", "child": branch.short_name}, 'branch': branch, 'form': form,
                   'cafedras': branch.cafedra_set.all(), 'add_cafedra_form': CafedraForm()}
        return render(request, 'branch_edit.html', context=context)
    else:
        return redirect('branch_detail', pk=pk)



@login_required
def branch_edit_view(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    employee = request.user.employee
    if employee and employee.branch == branch:
        if request.method == 'POST':
            form = BranchForm(request.POST, instance=branch)
            if form.is_valid():
                form.save()
                return redirect('branch_detail', pk=pk)
        else:
            form = BranchForm(instance=branch)
        context = {"breadcrumb": {"parent": "Филиалы", "child": branch.short_name}, 'branch': branch, 'form': form,
                   'cafedras': branch.cafedra_set.all()}
        return render(request, 'branch_edit.html', context=context)
    else:
        return redirect('branch_detail', pk=pk)


def user_profile(request):
    user = request.user
    employee = Employee.objects.get(user=user)
    positions = Position.objects.all()

    if request.method == 'POST':
        user_form = ErpUserForm(request.POST, instance=user)
        employee_form = EmployeeForm(request.POST, instance=employee)

        if user_form.is_valid() and employee_form.is_valid():
            user_form.save()
            employee_form.save()
            return redirect('user_profile')
    else:
        user_form = ErpUserForm(instance=user)
        employee_form = EmployeeForm(instance=employee)

    password_form = PasswordChangeForm(user)

    context = {
        'user': user,
        'employee': employee,
        'positions': positions,
        'user_form': user_form,
        'employee_form': employee_form,
        'password_form': password_form,
    }

    return render(request, 'user_profile.html', context)

def change_password(request):
    user = request.user
    employee = Employee.objects.get(user=user)
    positions = Position.objects.all()

    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменён.')
            return redirect('user_profile')
        else:
            for error in password_form.errors.values():
                for msg in error:
                    messages.error(request, msg)
    else:
        password_form = PasswordChangeForm(request.user)

    context = {
        'user': user,
        'employee': employee,
        'positions': positions,
        'password_form': password_form,
    }

    return render(request, 'user_password_change.html', context)



