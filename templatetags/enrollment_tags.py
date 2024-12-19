from account.models import Test_Series_Enrolment,Course_Enrolment,Mains_Test_Series_Enrolment
from django.template import Library
from datetime import datetime
from tseries.models import Series
from django.db.models import Q
from course.models import Course
from mains_test_series.models import Mains_Test_Series
 
register = Library()
 
@register.filter(name='check_enrollment')
def check_enrollment(value,user):
    if user.groups.filter(name='Instructor').exists():
        if Series.objects.filter(Q(created_by=user) | Q(moderator=user),id=value).exists():
            return True
        else:
            return False      
           
    if Test_Series_Enrolment.objects.filter(series=value,user=user).exists():        
        return True
    else:
        return False  

@register.filter(name='check_mains_enrollment')
def check_mains_enrollment(value,user):

    if user.groups.filter(name='Instructor').exists():
        if Mains_Test_Series_Enrolment.objects.filter(Q(created_by=user) | Q(moderator=user),id=value).exists():
            return True
        else:
            return False      
           
    if Mains_Test_Series_Enrolment.objects.filter(series=value,user=user).exists():        
        return True
    else:
        return False 


@register.filter(name='check_course_enrollment')
def check_course_enrollment(value,user):

    if user.groups.filter(name='Instructor').exists():
        if Course.objects.filter(Q(created_by=user) | Q(moderator=user),id=value).exists():
            return True
        else:
            return False    
     
         
    
    if Course_Enrolment.objects.filter(course=value,user=user).exists():        
        return True
    else:
        return False  





           
  
    
 
  