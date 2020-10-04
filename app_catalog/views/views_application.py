from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from app_catalog.forms import ApplicationForm
from app_catalog.models import Vacancy


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'

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


class SentView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'sent.html'
