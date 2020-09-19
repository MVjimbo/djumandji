"""djumandji URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from app_catalog.views import MainView, VacancyListView, SpecialtyView, CompanyView, VacancyView, custom_404, \
    custom_500, MySignUpView, MyLogInView, MyLogOutView, MyCompanyView, MyCompanyView, MyCompanyCreateView

handler500 = custom_500
handler404 = custom_404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name="main"),
    path('vacancies/', VacancyListView.as_view(), name="vacancy_list"),
    re_path(r'^vacancies/(?P<pk>\d+)/$', VacancyView.as_view(), name="vacancy"),
    re_path(r'^vacancies/cat/(?P<category>\w+)/$', SpecialtyView.as_view(), name="category"),
    re_path(r'^companies/(?P<pk>\d+)/$', CompanyView.as_view(), name="company"),
    path('mycompany/', MyCompanyView.as_view(), name='mycompany'),
    path('mycompany/create/', MyCompanyCreateView.as_view(), name='mycompany_create')
]

urlpatterns += [
    path('register/', MySignUpView.as_view(), name='signup'),
    path('login/', MyLogInView.as_view(), name='login'),
    path('logout/', MyLogOutView.as_view(), name='logout')
]
