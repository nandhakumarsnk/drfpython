# Generated by Django 4.2.3 on 2023-08-19 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0027_remove_customuser_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave_entitlement',
            name='emp_id',
        ),
        migrations.RemoveField(
            model_name='leave_entitlement',
            name='leave_id',
        ),
        migrations.DeleteModel(
            name='Emp_Master',
        ),
        migrations.DeleteModel(
            name='Leave_Entitlement',
        ),
    ]