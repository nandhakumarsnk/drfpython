# Generated by Django 4.2.3 on 2023-09-11 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0051_alter_emp_leaves_mg_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='taken',
        ),
    ]
