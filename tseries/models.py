from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django import forms


enrollment_options = (('','Choose Enrollment Status'),('R','Registered'),('E','Enrolled'),('T','Trial'))

# Create your models here.


class Series(models.Model):    
    title=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True)
    start_date=models.DateField()
    end_date=models.DateField()
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='creators')
    moderator=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)
    active=models.BooleanField(default=False)
    lesson_plan=models.FileField(null=True,blank=True)

    def __str__(self):
        return self.title

    def clean(self):        
        if self.start_date > self.end_date:
            raise forms.ValidationError("End date should be greater than start date.")
            
    class Meta:
        verbose_name = 'Prelims Test Series'
        verbose_name_plural = 'Prelims Test Series'