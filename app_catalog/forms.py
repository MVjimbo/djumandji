from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from django.forms import Textarea, NumberInput, Select
from django.forms.widgets import Input

from app_catalog.models import Company, Application, Vacancy


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        widgets = {
            'written_username': Input(attrs={'class': 'form-control'}),
            'written_phone': Input(attrs={'class': 'form-control'}),
            'written_cover_letter': Textarea(attrs={'rows': 8, 'class': 'form-control'}),
        }
        # written_username = models.CharField(max_length=128)
        # written_phone = models.CharField(max_length=16)
        # written_cover_letter = models.TextField()
        # vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
        # user


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'location', 'description', 'employee_count')
        widgets = {
            'name': Input(attrs={'class': 'form-control'}),
            'location': Input(attrs={'class': 'form-control'}),
            'employee_count': Input(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'rows': 4, 'class': 'form-control', 'style': "color:#000;"}),
        }
        labels = {
            'name': 'Название компании',
            'location': 'География',
            'logo': 'Логотип',
            'description': 'Информация о компании',
            'employee_count': 'Количество человек в компании'
        }


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max')
        widgets = {
            'title': Input(attrs={'class': 'form-control'}),
            'salary_min': NumberInput(attrs={'class': 'form-control'}),
            'salary_max': NumberInput(attrs={'class': 'form-control'}),
            'specialty': Select(attrs={'class': 'form-control'}),
            'skills': Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 13})
        }

    def clean_salary_max(self):
        salary_min = self.cleaned_data['salary_min']
        salary_max = self.cleaned_data['salary_max']
        if salary_min > salary_max:
            raise forms.ValidationError('Минимальная зарплата должна быть меньше максимальной.')
        return salary_max
    # speciality = forms.ChoiceField(widget=Select(attrs={'class': 'custom-select'}), choices=SpecialtyChoices)
        # title = models.CharField(max_length=64)
        # specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, related_name="vacancies", null=True)
        # company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
        # skills = models.TextField()
        # description = models.TextField()
        # salary_min = models.IntegerField()
        # salary_max = models.IntegerField()
        # published_at = models.DateField()
