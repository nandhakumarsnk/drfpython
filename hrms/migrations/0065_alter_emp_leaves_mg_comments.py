# Generated by Django 4.2.3 on 2023-09-13 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0064_alter_emp_leaves_mg_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emp_leaves',
            name='mg_comments',
            field=models.CharField(default='Waiting for manager confirmation', max_length=500),
        ),
    ]
