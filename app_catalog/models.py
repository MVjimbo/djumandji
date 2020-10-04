import os

from django.contrib.auth.models import User
from django.db import models

from djumandji.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Specialty(models.Model):
    # – Код(code)
    # например, testing, gamedev
    # – Название(title)
    # – Картинка(picture)(пока
    # оставьте
    # пустой
    # строкой)
    class SpecialtyChoices(models.TextChoices):
        frontend = 'Фронтенд'
        backend = 'Бэкенд'
        gamedev = 'Геймдев'
        devops = 'Девопс'
        design = 'Дизайн'
        products = 'Продукты'
        management = 'Менеджмент'
        testing = 'Тестирование'

    code = models.CharField(max_length=32)
    title = models.CharField(max_length=32, choices=SpecialtyChoices.choices)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR, null=True)

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        self.picture.storage.delete(self.picture.path)
        super().delete(using, keep_parents)


def company_logo_path(instance, file):
    filename, file_extension = os.path.splitext(file)
    company_id = instance.id
    new_filename = 'logo' + str(company_id) + file_extension
    return os.path.join(MEDIA_COMPANY_IMAGE_DIR, new_filename)


class Company(models.Model):
    # – Название(name)
    # – Город(location)
    # – Логотипчик(logo)(пока
    # оставьте
    # пустой
    # строкой)
    # – Информация
    # о
    # компании(description)
    # – Количество
    # сотрудников(employee_count)
    name = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    logo = models.ImageField(upload_to=company_logo_path, null=True)
    description = models.TextField()
    employee_count = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company', default=None, null=True)

    def delete(self, using=None, keep_parents=False):
        self.logo.storage.delete(self.logo.path)
        super().delete(using, keep_parents)


class Vacancy(models.Model):
    # – Название
    # вакансии(title)
    # – Специализация(specialty) – связь
    # с
    # Specialty, укажите
    # related_name = "vacancies"
    # – Компания(company) – связь
    # с
    # Company, укажите
    # related_name = "vacancies"
    # – Навыки(skills)
    # – Текст(description)
    # – Зарплата
    # от(salary_min)
    # – Зарплата
    # до(salary_max)
    # – Опубликовано(published_at)

    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, related_name="vacancies", null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()


class Application(models.Model):
    # – Имя(written_username)
    # – Телефон(written_phone)
    # – Сопроводительное
    # письмо(written_cover_letter)
    # – Вакансия(vacancy) – связь
    # с
    # Vacancy, укажите
    # related_name = "applications"
    # – Пользователь(user) – связь
    # с
    # User, укажите
    # related_name = "applications"
    written_username = models.CharField(max_length=128)
    written_phone = models.CharField(max_length=16)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')


class Resume(models.Model):
    # – Пользователь
    # – Имя(name)
    # – Фамилия(surname)
    # – Готовность
    # к
    # работе(status) – Не
    # ищу
    # работу – Рассматриваю
    # предложения – Ищу
    # работу
    # – Вознаграждение(salary)
    # – Специализация(specialty)
    # – Квалификация(grade)  – Стажер – Джуниор – Миддл – Синьор — Лид
    # – Образование(education)
    # – Опыт
    # работы(experience)
    # – Портфолио(portfolio)
    class StatusChoices(models.TextChoices):
        not_active = 1, 'Не ищу'
        checking = 2, 'Рассматриваю'
        active = 3, 'Ищу работу'

    class GradeChoices(models.TextChoices):
        intern = 1, 'Стажер'
        junior = 2, 'Джуниор'
        middle = 3, 'Миддл'
        senior = 4, 'Синьор'
        lead = 5, 'Лид'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=StatusChoices.choices)
    salary = models.IntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, related_name='resumes')
    grade = models.CharField(max_length=30, choices=GradeChoices.choices)
    education = models.TextField()
    experience = models.TextField()
