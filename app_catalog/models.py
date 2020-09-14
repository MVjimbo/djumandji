from django.db import models


class Specialty(models.Model):
    # – Код(code)
    # например, testing, gamedev
    # – Название(title)
    # – Картинка(picture)(пока
    # оставьте
    # пустой
    # строкой)
    code = models.CharField(max_length=32)
    title = models.CharField(max_length=32)
    picture = models.URLField()


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
    logo = models.URLField()
    description = models.CharField(max_length=128)
    employee_count = models.IntegerField()


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
    skills = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()
