from mcq_test.models import Response,Attempt,Test
from django.template import Library
from datetime import datetime
from django.db.models import Max
from django.db.models import Min
from django.db.models import Avg
from account.models  import User

 
register = Library()

@register.simple_tag
def check_highest_mark(test):
   
    try:
        mark = Test.objects.filter(id=test).aggregate(max_score=Max('attempt__score'))
        j=Attempt.objects.filter(test=test).values_list('user', 'score').order_by('score')[:1]
       
        user=User.objects.get(id=j)
      
        
        
     
        return mark['max_score'],user.first_name
    except:
        return False

@register.simple_tag

def check_lowest_mark(test):
   
    try: 
        mark = Test.objects.filter(id=test).aggregate(min_score=Min('attempt__score'))
        j=Attempt.objects.filter(test=test).values_list('user', flat=True).order_by('score')[:1]
        user=User.objects.get(id=j)
      
        
     
        return mark['min_score'],user.first_name
    except:
       
        return False