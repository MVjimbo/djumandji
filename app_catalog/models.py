from django.contrib.auth.models import User
from django.db import models


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
    picture = models.URLField()

    def __str__(self):
        return self.title


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
    logo = models.URLField(null=True)
    description = models.TextField()
    employee_count = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company', default=None, null=True)


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
