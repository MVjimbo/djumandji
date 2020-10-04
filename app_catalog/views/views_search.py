from django.views.generic import ListView

from app_catalog.models import Vacancy


class SearchView(ListView):
    model = Vacancy
    template_name = 'search.html'

    def get_queryset(self):
        search_value = self.request.GET.get('s')
        vacancies = Vacancy.objects.filter(title__icontains=search_value) | \
            Vacancy.objects.filter(description__icontains=search_value)
        return vacancies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_value'] = self.request.GET.get('s')
        return context
