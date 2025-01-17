from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from . import views
from .views import change_password

urlpatterns = [
    path('', views.index, name='index'),

    path('signup_home', views.signup_home, name='signup_home'),
    path('login_home', views.login_home, name="login_home"),
    path('logout_view', views.logout_view, name="logout_view"),
    path('core/organization', views.organization_view, name="organization_view"),
    path('core/employees', views.employee_list_view, name="employees"),
    path('api/v1/employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('core/branches', views.branch_list_view, name="branches"),
    path('core/branches/<int:pk>/', views.branch_detail_view, name='branch_detail'),
    path('core/branches/<int:pk>/edit/', views.branch_edit_view, name='branch_edit'),
    path('core/profile/user/<int:pk>/', views.view_user_profile, name='view_user_profile'),
    path('core/profile/', views.user_profile, name='user_profile'),
    path('change-password/', change_password, name='change_password'),
]

if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()