# Generated by Django 4.2.3 on 2023-09-05 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0046_delete_employee_documents'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee_documents',
            fields=[
                ('emp_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('educational_certificates', models.FileField(upload_to='educational_certificates/')),
                ('appointment_letter', models.FileField(upload_to='appointment_letter/')),
                ('passport_size_photo', models.FileField(upload_to='passport_size_photo/')),
                ('pancard', models.FileField(upload_to='pancards/')),
                ('aadharcard', models.FileField(upload_to='aadharcards/')),
            ],
        ),
    ]