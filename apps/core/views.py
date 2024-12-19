from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_page
from rest_framework import generics

from apps.core.forms import ErpUserForm, EmployeeForm, CafedraForm
from apps.core.models import Employee, Branch, Position
from apps.core.serializers import EmployeeSerializer


@login_required(login_url="/login_home")
# @cache_page(60 * 5)
def index(request):
    context = {"breadcrumb": {"parent": "Главная", "child": "Рабочий стол"}, "jsFunction": 'startTime()'}
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
def branch_detail(request, pk):
    branch = Branch.objects.get(pk=pk)
    user = request.user
    employee = Employee.objects.filter(user=user, branch=branch).first()
    if employee is None:
        return HttpResponseForbidden()
    cafedra_form = CafedraForm()
    context = {
        'cafedra_form': cafedra_form
    }
    return render(request, 'branch_detail.html', context)


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
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('user_profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'user_profile.html', {'form': form})



