import datetime

from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, FormView, ListView, UpdateView

from app_catalog.forms import CompanyForm, VacancyForm
from app_catalog.models import Company, Vacancy, Application


class MyCompanyView(FormView):
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
            return  redirect(reverse('mycompany_create'))# render(request, 'mycompany/company-edit.html', context={'form': CompanyForm})
        elif not Company.objects.filter(owner_id=user_id).exists():
            return render(request, 'mycompany/company-create.html')
        else:
            return redirect(reverse('mycompany_update'))# render(request, 'mycompany/company-edit.html', context={'form': CompanyForm})


class MyCompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'mycompany/company-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse('mycompany_create')
        return context

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST)
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


    # def form_valid(self, form):
        # company = form.save(commit=False)
        # company.owner = self.request.user
        # company.save()
        # Company.objects.create(name=form.cleaned_data.get('name'),
        #                        location=form.cleaned_data.get('location'),
        #                        employee_count=form.cleaned_data.get('employee_count'),
        #                        description=form.cleaned_data.get('description'),
        #                        owner=self.request.user)
        # return reverse('mycompany')


class MyCompanyUpdateView(FormView):
    form_class = CompanyForm
    template_name = 'mycompany/company-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse('mycompany_update')
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
        form = CompanyForm(request.POST)
        if form.is_valid():
            user = request.user
            if not Company.objects.filter(owner_id=user.id).exists():
                return redirect(reverse('mycompany'))
            Company.objects.filter(owner_id=user.id).update(
                name=form.cleaned_data.get('name'),
                location=form.cleaned_data.get('location'),
                description=form.cleaned_data.get('description'),
                employee_count=form.cleaned_data.get('employee_count')
            )
            return redirect(reverse('mycompany'))
        else:
            form.add_error('name', 'bruh')
            return render(request, 'mycompany/company-edit.html', context={'form': form, 'bruh': 'bruh'})


class MyCompanyVacancyListView(ListView):
    model = Vacancy
    template_name = 'mycompany/vacancy-list.html'

    def get_queryset(self):
        queryset = Vacancy.objects.filter(company__owner_id=self.request.user.id)\
            .annotate(count_applications=Count('applications'))
        return queryset


class VacancyCreate(FormView):
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


class MyCompanyVacancyView(FormView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'mycompany/vacancy-edit.html'
    # 'title': Input(attrs={'class': 'form-control'}),
    # 'salary_min': NumberInput(attrs={'class': 'form-control'}),
    # 'salary_max': NumberInput(attrs={'class': 'form-control'}),
    # 'specialty': Select(attrs={'class': 'form-control'}, choices=SpecialtyChoices),
    # 'skills': Textarea(attrs={'class': 'form-control', 'rows': 3}),
    # 'description': Textarea(attrs={'class': 'form-control', 'rows': 13})

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


class MyCompanyVacancyUpdateView(UpdateView):
    model = Vacancy
    form_class = VacancyForm
    pk_url_kwarg = 'vacancy_id'

    def get_success_url(self):
        return reverse('mycompany_vacancy', args=[self.kwargs.get(self.pk_url_kwarg)])
