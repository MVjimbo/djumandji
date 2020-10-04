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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from app_catalog.views.views_general import MainView, VacancyListView, SpecialtyView, CompanyView, VacancyView, \
    custom_404, custom_500
from app_catalog.views.views_resume import MyResumeView, MyResumeCreateView, MyresumeUpdateView
from app_catalog.views.views_search import SearchView
from app_catalog.views.views_user import MySignUpView, MyLogInView
from app_catalog.views.views_mycompany import MyCompanyView, MyCompanyCreateView, MyCompanyUpdateView, \
    MyCompanyVacancyListView, VacancyCreate, MyCompanyVacancyView
from app_catalog.views.views_application import ApplicationCreateView, SentView
from app_catalog.views.views_mycompany import MyCompanyVacancyUpdateView

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
    path('mycompany/create/', MyCompanyCreateView.as_view(), name='mycompany_create'),
    path('mycompany/update/', MyCompanyUpdateView.as_view(), name='mycompany_update'),
    path('mycompany/vacancies/', MyCompanyVacancyListView.as_view(), name='mycompany_vacancy_list'),
    re_path(r'^mycompany/vacancies/(?P<vacancy_id>\d+)/$', MyCompanyVacancyView.as_view(), name='mycompany_vacancy'),
    re_path(r'^mycompany/vacancies/(?P<vacancy_id>\d+)/update/$', MyCompanyVacancyUpdateView.as_view(),
            name='mycompany_vacancy_update'),
    path('vacancy/create/', VacancyCreate.as_view(), name='mycompany_vacancy_create'),
    path('application/create/', ApplicationCreateView.as_view(), name='application_create'),
    path('sent/', SentView.as_view(), name='sent'),
    path('search/', SearchView.as_view(), name='search'),
    path('myresume/', MyResumeView.as_view(), name='myresume'),
    path('myresume/create/', MyResumeCreateView.as_view(), name='myresume_create'),
    path('myresume/update/', MyresumeUpdateView.as_view(), name='myresume_update'),
]

urlpatterns += [
    path('register/', MySignUpView.as_view(), name='signup'),
    path('login/', MyLogInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
