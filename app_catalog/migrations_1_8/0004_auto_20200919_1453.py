# Generated by Django 3.0.3 on 2020-09-19 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0003_auto_20200919_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.URLField(null=True),
        ),
    ]
