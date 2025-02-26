# Generated by Django 3.1.1 on 2021-12-16 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20211214_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='miscellaneous_fee',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='miscellaneous_fee',
            name='type',
        ),
        migrations.AddField(
            model_name='miscellaneous_fee',
            name='paid_for',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='miscellaneous_fee',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
