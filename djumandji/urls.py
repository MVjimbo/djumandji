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
from django.urls import path

from app_catalog.views import MainView, VacancyListView, SpecialtyView, CompanyView, VacancyView, custom_404, custom_500

handler500 = custom_500
handler404 = custom_404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name="main"),
    path('vacancies/', VacancyListView.as_view(), name="vacancy_list"),
    path('vacancies/<int:pk>/', VacancyView.as_view(), name="vacancy"),
    path('vacancies/cat/<str:category>/', SpecialtyView.as_view(), name="category"),
    path('companies/<int:pk>/', CompanyView.as_view(), name="company")
]
