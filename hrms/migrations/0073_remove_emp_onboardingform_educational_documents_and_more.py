# Generated by Django 4.2.3 on 2023-09-20 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0072_emp_onboardingform_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emp_onboardingform',
            name='educational_documents',
        ),
        migrations.RemoveField(
            model_name='emp_onboardingform',
            name='photo',
        ),
    ]
