from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.defaults import page_not_found, server_error
from django.views.generic import DetailView, ListView, TemplateView, CreateView

from app_catalog.models import Vacancy, Company, Specialty
from app_catalog.forms import ApplicationForm, CompanyCreateForm


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


class VacancyView(DetailView):
    model = Vacancy
    template_name = "vacancy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application_form = ApplicationForm(self.request)
        context["application_form"] = application_form
        return context


class MySignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'user/signup.html'
    success_url = '/'
    
    # def get(self, request, *args, **kwargs):
    #     self.success_url = request.META.get('HTTP_REFERER')
    #     return super(MySignUpView, self).get(request, *args, **kwargs)


class MyLogInView(LoginView):
    template_name = "user/login.html"
    redirect_authenticated_user = True

    # def get_success_url(self):
    #     url = self.request.META.get('HTTP_REFERER')
    #     print(url)
    #     return '/'


class MyLogOutView(LogoutView):
    pass


class MyCompanyView(TemplateView):
    # def get_template_names(self):#(self, request, *args, **kwargs):
    #     user_id = self.request.user.id
    #     if Company.objects.filter(owner_id=user_id) and \
    #             self.request.META.get('HTTP_REFERER').find(reverse('mycompany')) != -1:
    #         return 'mycompany/company-edit.html'
    #     return 'mycompany/company-create.html'

    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        if not Company.objects.filter(owner_id=user_id).exists() and \
                self.request.META.get('HTTP_REFERER').find(reverse('mycompany')) != -1:
            return render(request, 'mycompany/company-edit.html', context={'form': CompanyCreateForm})
        elif not Company.objects.filter(owner_id=user_id).exists():
            return render(request, 'mycompany/company-create.html')
        else:
            return render(request, 'mycompany/company-edit.html', context={'form': CompanyCreateForm})


class MyCompanyCreateView(CreateView):
    def post(self, request, *args, **kwargs):
        form = CompanyCreateForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = self.request.user
            company.save()
            return redirect(reverse('mycompany'))
        else:
            form.add_error('name', 'bruh')
            return render(request, 'mycompany/company-edit.html', context={'form': form})


    # def form_valid(self, form):
        # company = form.save(commit=False)
        # company.owner = self.request.user
        # company.save()
        # Company.objects.create(name=form.cleaned_data.get('name'),
        #                        location=form.cleaned_data.get('location'),
        #                        employee_count=form.cleaned_data.get('employee_count'),
        #                        description=form.cleaned_data.get('description'),
        #                        owner=self.request.user)
        return reverse('mycompany')


    # def post(self, request, *args, **kwargs):

