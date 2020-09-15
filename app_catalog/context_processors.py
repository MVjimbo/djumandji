from django.urls import reverse


def menu(request):
    kwargs = {
        "main_part_of_menu": {
            "title": "Джуманджи",
            "link": "/"
        },
        "parts_of_menu": [
            {
                "title": "Вакансии",
                "link": reverse("vacancy_list")
            },
            {
                "title": "Компании",
                "link": "#",
            },
            {
                "title": "О проекте",
                "link": "#"
            }
        ]
    }
    return kwargs
