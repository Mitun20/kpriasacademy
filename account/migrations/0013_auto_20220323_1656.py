# Generated by Django 3.1.1 on 2022-03-23 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20211216_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('email', models.EmailField(max_length=254)),
                ('mobile_number', models.CharField(max_length=20)),
                ('alternate_mobile_number', models.CharField(max_length=20, null=True)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Enquirie',
            },
        ),
        migrations.AlterModelOptions(
            name='course_enrolment',
            options={'ordering': ('user__admission_number',), 'verbose_name_plural': 'Course Enrolment'},
        ),
        migrations.AddField(
            model_name='user',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='hostel_fees',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='hostel_fees_paid_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='merit',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='received_amount',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='regular',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='study_hall',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='weekend',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='hostel',
            field=models.BooleanField(default=False),
        ),
    ]