# Generated by Django 4.2.3 on 2023-09-13 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0063_customuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emp_leaves',
            name='mg_comments',
            field=models.CharField(default='Waiting for manager conformation', max_length=500),
        ),
    ]
