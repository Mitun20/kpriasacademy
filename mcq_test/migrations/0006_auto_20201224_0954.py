# Generated by Django 3.1.1 on 2020-12-24 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcq_test', '0005_auto_20201104_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
