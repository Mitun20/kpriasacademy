from django.db import models

from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Scholarship_Test(models.Model):    
    title=models.CharField(max_length=30)
    description=models.TextField()
    open_date=models.DateTimeField()
    close_date=models.DateTimeField()
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='scholarship_created_by')
    moderator=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)
    active=models.BooleanField(default=False)


    def __str__(self):
        return self.title
   


    class Meta:
        verbose_name = 'Scholarship Test'
        verbose_name_plural = 'Scholarship Test'

