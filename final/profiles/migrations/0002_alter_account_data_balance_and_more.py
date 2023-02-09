# Generated by Django 4.1.6 on 2023-02-08 19:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_data',
            name='Balance',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='customer_data',
            name='Phone_no',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Amount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]