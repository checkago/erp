from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('signup_home', views.signup_home, name='signup_home'),
    path('login_home', views.login_home, name="login_home"),
    path('logout_view', views.logout_view, name="logout_view"),
    path('core/employees', views.employee_list_view, name="employees"),
    path('api/v1/employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('core/branches', views.branch_list_view, name="branches"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
