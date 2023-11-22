# Generated by Django 4.2.4 on 2023-08-16 19:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0019_delete_emp_leaves'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emp_leaves',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('leave_balance', models.IntegerField(blank=True, null=True)),
                ('no_of_days', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(default='Approval Pending', max_length=50)),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('leave_typename', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hrms.leavetype')),
            ],
        ),
    ]
