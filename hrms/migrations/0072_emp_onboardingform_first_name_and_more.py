# Generated by Django 4.2.3 on 2023-09-20 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0071_rename_name_emp_onboardingform_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='emp_onboardingform',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='emp_onboardingform',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]