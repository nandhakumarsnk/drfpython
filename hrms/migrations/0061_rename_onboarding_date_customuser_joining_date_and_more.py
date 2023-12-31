# Generated by Django 4.2.3 on 2023-09-13 06:24

from django.db import migrations, models
import hrms.models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0060_alter_customuser_aadhar_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='onboarding_date',
            new_name='joining_date',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='address',
        ),
        migrations.AddField(
            model_name='customuser',
            name='work_location',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employee_documents',
            name='aadharcard',
            field=models.FileField(upload_to=hrms.models.generate_filename1),
        ),
        migrations.AlterField(
            model_name='employee_documents',
            name='appointment_letter',
            field=models.FileField(upload_to=hrms.models.generate_filename1),
        ),
        migrations.AlterField(
            model_name='employee_documents',
            name='educational_certificates',
            field=models.FileField(upload_to=hrms.models.generate_filename1),
        ),
        migrations.AlterField(
            model_name='employee_documents',
            name='pancard',
            field=models.FileField(upload_to=hrms.models.generate_filename1),
        ),
        migrations.AlterField(
            model_name='employee_documents',
            name='passport_size_photo',
            field=models.FileField(upload_to=hrms.models.generate_filename1),
        ),
    ]
