from mcq_test.models import Test
from django.template import Library
from datetime import datetime

 
register = Library()
 
@register.filter(name='check_response_status')
def check_response_status(value, user):
 

    
    if not Test.objects.filter(id=value,close_date__gte=datetime.today()).exists() :               
        return True
    else:        
        return False  



@register.simple_tag
def multiple_args_tag(a, b, c, d):
   print(a)
   
   return True



           
  
    
 
  