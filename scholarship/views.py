from django.shortcuts import render
from mcq_test.models import Test,Attempt, On_Test,Question
from account.models import Scholarship_Test_Enrolment
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from account.views import complete_profile
# Create your views here.


@complete_profile
def scholarship(request): 
    test=Test.objects.filter(scholarship_test__isnull=False,open_date__lte=datetime.today(), close_date__gte=datetime.today(),active=True).order_by('open_date').exclude(attempt__user=request.user)       
    return render(request, 'Scholarship/scholarship_test_list.html', {'test':test,})



@complete_profile
@login_required(login_url='login') 
def test(request,test):
    

    if Attempt.objects.filter(test=test,user=request.user).exists():
        return HttpResponse("No More attempts allowed")


    if not On_Test.objects.filter(user=request.user).exists():
        On_Test.objects.create(user=request.user,test_id=test,started_time=datetime.now())

    old_one=[]

    current_test=Test.objects.get(id=test)
    old_test=On_Test.objects.get(user=request.user)   
 
    if current_test.id == old_test.test.id:
        then = old_test.started_time
        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S') 
        diff = (now - then).total_seconds()       
        mins = current_test.duration_in_minutes - ((diff // 60) + 1)
        seconds = 59 - diff % 60

        test_object=Test.objects.get(id=test,scholarship_test__isnull=False)
     
        questions=list(test_object.question.values_list('id',flat=True))
        
        question = Question.objects.get(id=questions[0])
  
               
        context={
                'sorted_questions' : questions,
                'question_count' : len(questions),
                'question_no' : 0,
                'question' : question,
                'test':test_object,
                'question_next' : 1,
                'question_prev' : -1,
                'mins':mins,
                'seconds':seconds
            
             }
        return render(request, 'Scholarship/test.html', context)
   
    elif current_test.id != old_test.test.id:
        return  render(request, 'test/old_test.html', {'old_test':old_test,'current_test':current_test,})



@complete_profile
def scholarship_test_submission(request):
    return render(request, 'Scholarship/submission.html', {})