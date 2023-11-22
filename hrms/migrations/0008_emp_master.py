# Generated by Django 4.2.4 on 2023-08-10 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0007_leavetype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emp_Master',
            fields=[
                ('emp_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('reporting_to', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('is_user', models.BooleanField(default=False)),
            ],
        ),
    ]