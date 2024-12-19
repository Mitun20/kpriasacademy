from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from subject.models import Subject
from django.urls import reverse
from django.utils.safestring import mark_safe
from tseries.models import Series
from mains_test_series.models import Mains_Test_Series
from datetime import date


upse_status_options = (('','Choose Current Status of UPSC'),('Registered','Registered'),('Prelims Attempted','Prelims Attempted'),('Prelims Cleared','Prelims Cleared'),('Main Attempted','Main Attempted'),('Main Cleared','Main Cleared'),('Interview  Attempt','Interview  Attempt'),('Rank','Rank'),('all','all'))
test_options=(('','Choose Test Type'),('P','Prelims'),('M','Mains'))


class Batch(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Create your models here.
class Course(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    open_date=models.DateTimeField()
    close_date=models.DateTimeField()
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='course_created_by')
    moderator=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)
    active=models.BooleanField(default=False)
    lesson_plan=models.FileField(null=True,blank=True,upload_to='course',verbose_name="Brochure")
    prelims_test_series=models.ForeignKey(Series,on_delete=models.SET_NULL,null=True,blank=True)
    mains_test_series=models.ForeignKey(Mains_Test_Series,on_delete=models.SET_NULL,null=True,blank=True)


    def __str__(self):
        return self.title


class Part(models.Model):
    title=models.CharField(max_length=30)
    description=models.TextField(null=True,blank=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    test_type=models.CharField(choices=test_options,max_length=20,null=True,blank=True)

    def __str__(self):
        return self.title

    def part_changeform_link(self):
        if self.id:
            
            changeform_url = reverse(
            'admin:course_part_change', args=(self.id,)
            )
            return mark_safe(u'<a href="%s" target="_blank">View Part</a>' % changeform_url)
        return u''
    part_changeform_link.allow_tags = True
    part_changeform_link.short_description = '' 



class Topic(models.Model):
    name=models.CharField(max_length=30)
    part=models.ForeignKey(Part,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)

    def __str__(self):
        return self.name



    def changeform_link(self):
        if self.id:
            
            changeform_url = reverse(
            'admin:course_topic_change', args=(self.id,)
            )
            return mark_safe(u'<a href="%s" target="_blank">View Topic</a>' % changeform_url)
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''


'''
class Class_Test(models.Model):
    title=models.CharField(max_length=50,null=True)
    part=models.ForeignKey(Part,on_delete=models.CASCADE)
    description=models.TextField()

    def __str__(self):
        return self.title

    def class_changeform_link(self):
        if self.id:
            
            changeform_url = reverse(
            'admin:course_class_test_change', args=(self.id,)
            )
            return mark_safe(u'<a href="%s" target="_blank">View Class Test</a>' % changeform_url)
        return u''
    class_changeform_link.allow_tags = True
    class_changeform_link.short_description = ''
    
'''

class Live_Sessions(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    start_date_time=models.DateTimeField()
    end_date_time=models.DateField()
    link=models.URLField(max_length=200)
    password_if_any=models.CharField(max_length=30,blank=True)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE,null=True)


    class Meta:
        verbose_name="Live Session"    

class Video(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    link =  models.CharField(max_length=255)
    close_date=models.DateField(default=None)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE,null=True)



    @property
    def date_comparing(self):
        if self.close_date >= date.today():            
            return True
        else:
            return False

    class Meta:
        ordering = ['id']


class Material(models.Model):
    title=models.CharField(max_length=50,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    material = models.FileField(upload_to='profile_photo/material')

    class Meta:
        ordering = ['id']


    @property
    def material_url(self):
        if self.material:
            return self.material.url 




    
