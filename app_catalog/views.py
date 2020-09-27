from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.defaults import page_not_found, server_error
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, FormView

from app_catalog.models import Vacancy, Company, Specialty
from app_catalog.forms import ApplicationForm, CompanyForm
from app_catalog.views_add.views_mycompany import MyCompanyView, MyCompanyCreateView, MyCompanyUpdateView, \
    MyCompanyVacancyListView, VacancyCreate, MyCompanyVacancyView, MyCompanyVacancyUpdateView


def custom_404(request, exception):
    template_name = "errors/404.html"
    return page_not_found(request, exception, template_name)


def custom_500(request):
    template_name = "errors/500.html"
    return server_error(request, template_name)


class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_list"] = Company.objects.annotate(count=Count("vacancies"))
        context["specialty_list"] = Specialty.objects.annotate(count=Count("vacancies")).filter(count__gt=0)
        return context


class VacancyListView(ListView):
    model = Vacancy
    template_name = "vacancies.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count_vacancies"] = Vacancy.objects.count()
        return context


class SpecialtyView(ListView):
    template_name = "vacancies.html"

    def get_queryset(self):
        specialty_code = self.kwargs.get("category")
        vacancies = Vacancy.objects.filter(specialty__code=specialty_code)
        if not vacancies:
            raise Http404
        return vacancies

    def get_context_data(self, **kwargs):
        specialty_code = self.kwargs.get("category")
        context = super().get_context_data(**kwargs)
        context["count_vacancies"] = Vacancy.objects.filter(specialty__code=specialty_code).count()
        return context


class CompanyView(DetailView):
    model = Company
    template_name = "company.html"

    # def get_queryset(self):
    #     company_id = self.kwargs.get('pk')
    #     query_set = Vacancy.objects.filter(company_id=company_id)
    #     return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_id = self.kwargs.get('pk')
        vacancies = Vacancy.objects.filter(company_id=company_id)
        context["vacancies"] = vacancies
        return context


class VacancyView(DetailView, FormView):
    form_class = ApplicationForm
    model = Vacancy
    template_name = "vacancy.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     application_form = ApplicationForm(self.request)
    #     context["form"] = application_form
    #     return context


class MySignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'user/register.html'
    success_url = '/'
    
    # def get(self, request, *args, **kwargs):
    #     self.success_url = request.META.get('HTTP_REFERER')
    #     return super(MySignUpView, self).get(request, *args, **kwargs)


class MyLogInView(LoginView):
    template_name = "user/login1.html"
    redirect_authenticated_user = True


class ApplicationCreateView(CreateView):
    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)
        vacancy_id = request.POST.get('vacancy_id')
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            redirect(reverse(''))
        if form.is_valid():
            user = request.user
            application = form.save(commit=False)
            application.vacancy = vacancy
            application.user = user
            application.save()
            return redirect(reverse('sent'))
        else:
            return redirect(reverse('vacancy', args=[vacancy_id]))


class SentView(TemplateView):
    template_name = 'sent.html'
