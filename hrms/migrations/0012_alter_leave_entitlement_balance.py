# Generated by Django 4.2.4 on 2023-08-10 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0011_leave_entitlement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave_entitlement',
            name='balance',
            field=models.IntegerField(),
        ),
    ]
