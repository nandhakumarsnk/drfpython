# Generated by Django 4.2.3 on 2023-08-23 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0033_remove_customuser_entitlement_customuser_entitlement'),
    ]

    operations = [
        migrations.AddField(
            model_name='emp_leaves',
            name='application_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='application_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]