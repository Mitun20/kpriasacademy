from mcq_test.models import Response,Attempt
from django.template import Library
from datetime import datetime

from assignment.models import Submission

 
register = Library()
 
@register.simple_tag
def check_attempt(question_id, user, attempt):
    try:        
        status = Response.objects.get(question=question_id,attempt=attempt,user=user)        
        return status
    except:
        status =[]
        return status


@register.simple_tag
def check_mains_test_attempt(assignment_id, user, attempt):
    try:        
        status = Response.objects.get(question=question_id,attempt=attempt,user=user)        
        return status
    except:
        status =[]
        return status


@register.simple_tag
def check_attempt_daily_test(test_id, user):
    try:        
        status = Attempt.objects.get(test=test_id,user=user)        
        return status
    except:
        status =[]
        return status


@register.filter(name='check__daily_mcq_attempt')
def check__daily_mcq_attempt(value, user): 

    if Attempt.objects.filter(test=value,user=user).exists() :               
        return True
    else:        
        return False  



#for test series details page 


@register.filter(name='check_testseries_test_attempt')
def check_testseries_test_attempt(value, user): 

    if Attempt.objects.filter(test=value,user=user).exists() :               
        return "Attended"
    else:        
        return False  


@register.filter(name='check_mains_test_attempt')
def check_mains_test_attempt(value, user): 

    if Submission.objects.filter(assignment=value,user=user).exists():             
        return "Attended"
    else:        
        return False  




@register.filter(name='check_mains_submission_status')
def check_mains_submission_status(value, user): 

    if Submission.objects.filter(assignment=value,user=user,status="S").exists():
        return "Submitted"
    else:
        return None



@register.simple_tag
def mains_submitted_file_download(assignment_id, user):
    try:     
        submission = Submission.objects.get(assignment=assignment_id,user=user)
        return submission
    except:
        pass