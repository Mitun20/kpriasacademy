from django.db import models

from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Daily_Mcq(models.Model):
    title=models.CharField(max_length=30)
    description=models.TextField(null=True,blank=True)
    date=models.DateField()    
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='created_by')
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Daily Mcq"