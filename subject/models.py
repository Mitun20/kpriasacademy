from django.db import models

# Create your models here.



class Subject(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField(null=True,blank=True)


    def __str__(self):
        return self.name