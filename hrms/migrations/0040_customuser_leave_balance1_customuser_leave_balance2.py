# Generated by Django 4.2.3 on 2023-08-24 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0039_remove_customuser_leave_balance_type1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='leave_balance1',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='customuser',
            name='leave_balance2',
            field=models.PositiveIntegerField(default=15),
        ),
    ]