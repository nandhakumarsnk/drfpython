# Generated by Django 4.2.4 on 2023-08-16 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0012_alter_leave_entitlement_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave_Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('comments', models.CharField(max_length=200)),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('leave_typename', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hrms.leavetype')),
            ],
        ),
    ]
