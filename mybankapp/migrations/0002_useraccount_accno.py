# Generated by Django 5.0.2 on 2024-05-13 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybankapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='accno',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='mybankapp.useraccountnumber'),
        ),
    ]
