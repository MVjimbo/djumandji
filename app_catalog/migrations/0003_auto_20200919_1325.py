# Generated by Django 3.0.3 on 2020-09-19 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0002_auto_20200917_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='company',
            name='employee_count',
            field=models.CharField(max_length=20),
        ),
    ]
