# Generated by Django 4.2.3 on 2023-09-11 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0050_emp_leaves_mg_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emp_leaves',
            name='mg_comments',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]