# Generated by Django 2.2.16 on 2020-10-09 18:04

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('scholarship', '0001_initial'),
        ('tseries', '0001_initial'),
        ('course', '0001_initial'),
        ('subject', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('daily_mcq', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0)),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('value', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('answer_description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('mark', models.FloatField(default=2)),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='subject.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('instruction', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('open_date', models.DateTimeField()),
                ('close_date', models.DateTimeField()),
                ('total_no_questions', models.PositiveIntegerField(blank=True, null=True)),
                ('total_marks', models.PositiveIntegerField(blank=True, null=True)),
                ('duration_in_minutes', models.PositiveIntegerField(blank=True, null=True)),
                ('show_answers', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('discussion_video_link', models.URLField(blank=True, null=True)),
                ('negative_mark', models.BooleanField(default=True)),
                ('course_part', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.Part')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('daily_mcq', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='daily_mcq.Daily_Mcq')),
                ('question', models.ManyToManyField(blank=True, to='mcq_test.Question')),
                ('scholarship_test', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scholarship.Scholarship_Test')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subject.Subject')),
                ('test_series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tseries.Series')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcq_test.Attempt')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcq_test.Option')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcq_test.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='option',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcq_test.Question'),
        ),
        migrations.CreateModel(
            name='On_Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_time', models.DateTimeField(null=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcq_test.Test')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='attempt',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcq_test.Test'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
