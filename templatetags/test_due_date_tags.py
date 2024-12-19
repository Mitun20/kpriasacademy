from mcq_test.models import Test,Attempt
from django.template import Library
from datetime import datetime
from assignment.models import Assignment,Submission

 
register = Library()
 
@register.filter(name='check_due_date')
def check_due_date(value,user):   
    if Attempt.objects.filter(user=user,test=value).exists():
        return False
    
    test= Test.objects.get(id=value)
    if test.open_date >= datetime.now():            
        return "Not Opened"
    elif test.close_date <= datetime.now():
                
        return "Over Due"  

@register.filter(name='check_assignment_due_date')
def check_assignment_due_date(value,user): 
    if not Submission.objects.filter(user=user,assignment=value).exists():

        assignment= Assignment.objects.get(id=value)
        if assignment.open_date >= datetime.now():
            return "Not Opened"
        elif assignment.close_date <= datetime.now():   
            return "Over Due"  
        

@register.filter(name='check_assignment_submission')
def check_assignment_submission(value,user): 
    if Submission.objects.filter(user=user,assignment=value,status="S").exists():
        return "Submitted"
 
        
        

@register.filter(name='check_assignment_result')
def check_assignment_result(value,user): 
    if Submission.objects.filter(user=user,assignment=value,status="A").exists():
        return "Accepted"
   
        
@register.filter(name='check_attempt_count')
def check_attempt_count(value,user):
    count=Attempt.objects.filter(test=value,user=user)
    return len(count)

@register.filter(name="zero_attempt_count")
def zero_attempt_count(value,user):
    if not Attempt.objects.filter(test=value,user=user).exists():
        return True


@register.simple_tag
def check_zero_attempt_close_date(test,user):

    if not  Attempt.objects.filter(test=test,user=user).exists():
        
        test= Test.objects.get(id=test)
        
    
        if test.open_date <= datetime.now():
            return True
        return False

    
    return None
  
    
 

 
  

@register.simple_tag
def check_attempt_close_date(test,user,close_date):

    if not  Attempt.objects.filter(test=test,user=user).exists():
        
        test= Test.objects.get(id=test)
        
    
        if test.open_date <= datetime.now():
            print("hello world")
            return True
        return False

    
    return None
  