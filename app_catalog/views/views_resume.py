from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, CreateView

from app_catalog.forms import ResumeForm
from app_catalog.models import Resume


class MyResumeView(LoginRequiredMixin, FormView):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        if not Resume.objects.filter(user_id=user_id).exists() and \
                self.request.META.get('HTTP_REFERER').find(reverse('myresume')) != -1:
            return redirect(reverse('myresume_create'))# render(request, 'mycompany/company-edit.html', context={'form': CompanyForm})
        elif not Resume.objects.filter(user_id=user_id).exists():
            return render(request, 'resume/resume-create.html')
        else:
            return redirect(reverse('myresume_update'))# render(request, 'mycompany/company-edit.html', context={'form': CompanyForm})


class MyResumeCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Resume
    form_class = ResumeForm
    template_name = 'resume/resume-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse('myresume_create')
        return context

    def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST)
        if form.is_valid():
            user = request.user
            if Resume.objects.filter(user_id=user.id).exists():
                return redirect(reverse('myresume'))
            resume = form.save(commit=False)
            resume.user = user
            resume.save()
            return redirect(reverse('myresume'))
        else:
            form.add_error('name', 'bruh')
            return render(request, 'resume/resume-edit.html', context={'form': form})


class MyresumeUpdateView(LoginRequiredMixin, FormView):
    login_url = '/login/'
    form_class = ResumeForm
    template_name = 'resume/resume-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse('myresume_update')
        return context

    def get_initial(self):
        initial = super().get_initial()
        myresume = Resume.objects.filter(user_id=self.request.user.id).first()
        initial['name'] = myresume.name
        initial['surname'] = myresume.surname
        initial['salary'] = myresume.salary
        initial['education'] = myresume.education
        initial['experience'] = myresume.experience
        return initial

    def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST)
        if form.is_valid():
            user = request.user
            try:
                resume = Resume.objects.get(user_id=user.id)
                resume.name = form.cleaned_data.get('name')
                resume.surname = form.cleaned_data.get('surname')
                resume.salary = form.cleaned_data.get('salary')
                resume.specialty = form.cleaned_data.get('specialty')
                resume.grade = form.cleaned_data.get('grade')
                resume.education = form.cleaned_data.get('education')
                resume.experience = form.cleaned_data.get('experience')
                resume.save()
            except:
                return redirect(reverse('myresume'))
            return redirect(reverse('myresume'))
        else:
            form.add_error('name', 'bruh')
            return render(request, 'resume/resume-edit.html', context={'form': form, 'bruh': 'bruh'})
