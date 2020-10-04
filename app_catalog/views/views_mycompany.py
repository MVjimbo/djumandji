import datetime
from os import remove

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, FormView, ListView, UpdateView

from app_catalog.forms import CompanyForm, VacancyForm
from app_catalog.models import Company, Vacancy, Application


class MyCompanyView(LoginRequiredMixin, FormView):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        if not Company.objects.filter(owner_id=user_id).exists() and \
                self.request.META.get('HTTP_REFERER').find(reverse('mycompany')) != -1:
            return redirect(reverse('mycompany_create'))
            # render(request, 'mycompany/company-edit.html', context={'form': CompanyForm})
        elif not Company.objects.filter(owner_id=user_id).exists():
            return render(request, 'mycompany/company-create.html')
        else:
            return redirect(reverse('mycompany_update'))
            # render(request, 'mycompany/company-edit.html', context={'form': CompanyForm})


class MyCompanyCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Company
    form_class = CompanyForm
    template_name = 'mycompany/company-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse('mycompany_create')
        return context

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            if Company.objects.filter(owner_id=user.id).exists():
                return redirect(reverse('mycompany'))
            company = form.save(commit=False)
            company.owner = user
            company.save()
            return redirect(reverse('mycompany'))
        else:
            form.add_error('name', 'bruh')
            return render(request, 'mycompany/company-edit.html', context={'form': form})


class MyCompanyUpdateView(LoginRequiredMixin, FormView):
    login_url = '/login/'
    form_class = CompanyForm
    template_name = 'mycompany/company-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse('mycompany_update')
        try:
            company = Company.objects.get(owner_id=self.request.user.id)
            context['image'] = company.logo.url
        except:
            pass
        return context

    def get_initial(self):
        initial = super().get_initial()
        mycompany = Company.objects.filter(owner_id=self.request.user.id).first()
        initial['name'] = mycompany.name
        initial['location'] = mycompany.location
        initial['description'] = mycompany.description
        initial['employee_count'] = mycompany.employee_count
        return initial

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            try:
                company = Company.objects.get(owner_id=user.id)
                company.name = form.cleaned_data.get('name')
                company.location = form.cleaned_data.get('location')
                company.description = form.cleaned_data.get('description')
                company.employee_count = form.cleaned_data.get('employee_count')
                if form.cleaned_data.get('logo'):
                    # remove(company.logo.path)
                    company.logo = form.cleaned_data.get('logo')
                print(request.FILES)
                company.save()
            except:
                return redirect(reverse('mycompany'))
            return redirect(reverse('mycompany'))
        else:
            form.add_error('name', 'bruh')
            return render(request, 'mycompany/company-edit.html', context={'form': form, 'bruh': 'bruh'})


class MyCompanyVacancyListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Vacancy
    template_name = 'mycompany/vacancy-list.html'

    def get_queryset(self):
        queryset = Vacancy.objects.filter(company__owner_id=self.request.user.id) \
            .annotate(count_applications=Count('applications'))
        return queryset


class VacancyCreate(LoginRequiredMixin, FormView):
    login_url = '/login/'
    form_class = VacancyForm
    template_name = 'mycompany/vacancy-create.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user
            vacancy = form.save(commit=False)
            try:
                vacancy.company = Company.objects.get(owner_id=user.id)
            except Company.DoesNotExist:
                return redirect(reverse('login'))
            vacancy.published_at = datetime.date.today()
            vacancy.save()
            return redirect(reverse('mycompany_vacancy_list'))
        else:
            return redirect(reverse('vacancy_create'))


class MyCompanyVacancyView(LoginRequiredMixin, FormView):
    login_url = '/login/'
    model = Vacancy
    form_class = VacancyForm
    template_name = 'mycompany/vacancy-edit.html'

    def get_initial(self):
        initial = super().get_initial()
        vacancy_id = self.kwargs.get('vacancy_id')
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            raise Http404
        initial['title'] = vacancy.title
        initial['salary_min'] = vacancy.salary_min
        initial['salary_max'] = vacancy.salary_max
        initial['speciality'] = vacancy.specialty.id
        initial['skills'] = vacancy.skills
        initial['description'] = vacancy.description
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy_id = self.kwargs.get('vacancy_id')
        context['vacancy_id'] = vacancy_id
        context['application_list'] = Application.objects.filter(vacancy_id=vacancy_id)
        context['application_count'] = Application.objects.filter(vacancy_id=vacancy_id).count()
        return context


class MyCompanyVacancyUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Vacancy
    form_class = VacancyForm
    pk_url_kwarg = 'vacancy_id'

    def get_success_url(self):
        return reverse('mycompany_vacancy', args=[self.kwargs.get(self.pk_url_kwarg)])
