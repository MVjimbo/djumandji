from django.db.models import Count
from django.http import Http404
from django.views.defaults import page_not_found, server_error
from django.views.generic import DetailView, ListView, TemplateView

from app_catalog.models import Vacancy, Company, Specialty


def custom_404(request, exception):
    template_name = "404.html"
    return page_not_found(request, exception, template_name)


def custom_500(request):
    template_name = "500.html"
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
        specialty_id = self.kwargs.get("category")
        vacancies = Vacancy.objects.filter(specialty__code=specialty_id)
        if not vacancies:
            raise Http404
        return vacancies


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
