# Generated by Django 4.2.3 on 2023-09-12 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0058_customuser_address_customuser_marital_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='aadhar_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='pancard_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]