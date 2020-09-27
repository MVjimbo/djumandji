from django.contrib import admin

from app_catalog.models import Specialty, Company, Vacancy, Application


class CompanyVacancyInline(admin.TabularInline):
    model = Vacancy
    extra = 1


class SpecialtyVacancyInline(admin.TabularInline):
    model = Vacancy
    extra = 1


class VacancyApplicationInline(admin.TabularInline):
    model = Application
    extra = 1


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'picture')
    inlines = (SpecialtyVacancyInline, )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'employee_count', 'logo', 'description', 'owner')
    readonly_fields = ('owner', 'name', 'location', 'description', 'employee_count')
    inlines = (CompanyVacancyInline,)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'specialty', 'company', 'skills', 'description', 'salary_min', 'salary_max',
                    'published_at')
    readonly_fields = ('company', 'salary_min', 'salary_max', 'published_at')
    inlines = (VacancyApplicationInline, )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('written_username', 'written_phone', 'written_cover_letter', 'vacancy', 'user')
    readonly_fields = ('vacancy', 'user')

