from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import generics

from apps.core.models import Employee, Branch
from apps.core.serializers import EmployeeSerializer


@login_required(login_url="/login_home")
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
def employee_list_view(request):
    employees = Employee.objects.all()
    context = {"breadcrumb": {"parent": "Главная", "child": "Сотрудники"}, 'employees': employees}
    return render(request, 'employee_list.html', context=context)


class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


@login_required(login_url="/login_home")
def branch_list_view(request):
    branches = Branch.objects.all().order_by('short_name')
    context = {"breadcrumb": {"parent": "Главная", "child": "Филиалы"}, 'branches': branches}
    return render(request, 'branch_list.html', context=context)
