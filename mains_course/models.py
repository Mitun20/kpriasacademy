from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django import forms

# Create your models here.


class Course_Test_Series(models.Model):    
    title=models.CharField(max_length=50)
    description=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='mains_course_creators')
    moderator=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)
    active=models.BooleanField(default=False)
    lesson_plan=models.FileField(null=True,blank=True)

    def __str__(self):
        return self.title

    def clean(self):        
        if self.start_date > self.end_date:
            raise forms.ValidationError("End date should be greater than start date.")



    class Meta:
        verbose_name = 'Course Test Series'
        verbose_name_plural = 'Course Test Series'

