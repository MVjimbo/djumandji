import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'djumandji.settings')
django.setup()


from data import companies, jobs, specialties
from app_catalog.models import Company, Specialty, Vacancy


if __name__ == "__main__":
    Company.objects.bulk_create(
        [
            Company(
                name=company["title"],
                employee_count=0
            )
            for company in companies
        ]
    )

    Specialty.objects.bulk_create(
        [
            Specialty(
                code=specialty["code"],
                title=specialty["title"]
            )
            for specialty in specialties
        ]
    )

    vacancies = Vacancy.objects.bulk_create(
        [
            Vacancy(
                title=job["title"],
                salary_min=job["salary_from"],
                salary_max=job["salary_to"],
                published_at=job["posted"],
                description=job["desc"],
                company=Company.objects.get(name=job["company"]),
                specialty=Specialty.objects.get(code=job["cat"])
            )
            for job in jobs
        ]
    )
