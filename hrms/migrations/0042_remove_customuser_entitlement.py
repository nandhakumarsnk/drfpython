# Generated by Django 4.2.3 on 2023-09-01 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0041_remove_emp_leaves_leave_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='entitlement',
        ),
    ]