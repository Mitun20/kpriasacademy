from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from course.models import Course
from mains_test_series.models import Mains_Test_Series
from course.models import Part


submission_options = (('S','Not Evaluated'),('A','Evaluated'))

# Create your models here.
class Assignment(models.Model):    
    title = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    open_date = models.DateTimeField(null=True,blank=True)
    close_date = models.DateTimeField(null=True,blank=True)
    marks = models.IntegerField(null=True,blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    moderator=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="assignment_created_by",blank=True,null=True)
    test_series=models.ForeignKey(Mains_Test_Series,on_delete=models.CASCADE,null=True,blank=True)
    part=models.ForeignKey(Part,on_delete=models.CASCADE,null=True,blank=True)
    discussion_video_link=models.URLField(max_length=200,null=True,blank=True)
    
    def __str__(self):
        return self.title

    def changeform_link(self):
        if self.id:
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            changeform_url = reverse(
            'admin:assignment_assignment_change', args=(self.id,)
            )
            return mark_safe(u'<a href="%s" target="_blank">View Descriptive Test</a>' % changeform_url)
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Mains Test'




class AFile(models.Model):
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    afile = models.FileField(upload_to='descriptivetfile')

    @property
    def afile_url(self):
        if self.afile:
            return self.afile.url 
            
    class Meta:
        verbose_name = ' Question File'
        verbose_name_plural = 'Question File'



class Submission(models.Model):
    
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    status = models.CharField(choices=submission_options,max_length=1)
    submitted_on = models.DateTimeField(auto_now_add=True)
    marks = models.IntegerField()
    corrected_answer_sheet=models.FileField(blank=True,null=True)
    sfile = models.FileField(null=True,upload_to='descriptivetfile')

    def __str__(self):
        return self.assignment.title


    def changeform_link(self):
        if self.id:
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            changeform_url = reverse(
            'admin:assignment_submission_change', args=(self.id,)
            )
            return mark_safe(u'<a href="%s" target="_blank">View Submissions</a>' % changeform_url)
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''