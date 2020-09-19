from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from django.forms import Textarea
from django.forms.widgets import Input

from app_catalog.models import Company


class ApplicationForm(forms.Form):
    user = forms.CharField(min_length=1, max_length=10000)
    telephone = forms.CharField(max_length=12, )
    letter = forms.CharField(widget=forms.Textarea)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.form_class = "mt-5"
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'

        self.helper.layout = Layout(
            Fieldset(
                'Подать заявку',
                AppendedText('user', '', 'ваше имя'),
                PrependedText('telephone', '&#128222;', '+00000000000'),
                AppendedText('letter', '', 'ваше описание')
            ),
            FormActions(
                Submit('submit', 'Отправить')
            )
        )


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'location','description', 'employee_count')
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
