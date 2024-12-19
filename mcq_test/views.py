from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from tseries.models import Series
from account.models import Test_Series_Enrolment
from .models import Test,Question,Response,On_Test
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import Attempt
from datetime import datetime, date, timedelta
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from account.views import complete_profile


# Create your views here.
@complete_profile
@login_required(login_url='login') 
def test_series_list(request):    
    series=Series.objects.filter(start_date__lte=date.today(), end_date__gte=date.today(),active=True).order_by('-start_date')       
    return render(request, 'test/test_series_list.html', {'series':series,})


@complete_profile
@login_required(login_url='login')
def test_series_detail(request,series):      
    if Test_Series_Enrolment.objects.filter(series=series,user=request.user).exists() or request.user.groups.filter(name='Instructor').exists():
        test= Test.objects.filter(test_series=series,active="True").order_by('open_date') 
        return render(request, 'test/view_test_series.html', {'test':test,})

    return HttpResponse("You don't have rights to access the test series")


@complete_profile
@login_required(login_url='login') 
def view_instruction(request,test):
    
    if Test_Series_Enrolment.objects.filter(series__test=test,user=request.user,series__test__open_date__lte=datetime.now(),series__test__close_date__gte=datetime.now(),series__test__active="True").exists() or request.user.groups.filter(name='Instructor').exists():
        test=Test.objects.get(id=test)
        return render(request, 'test/view_instruction.html', {'test':test,})

    return HttpResponse("You don't have rights to view the instruction")


@complete_profile
@login_required(login_url='login') 
def test(request,test):

    test_object=Test.objects.get(id=test)
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


        test_object=Test.objects.get(id=test,test_series__isnull=False)
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
        return render(request, 'test/test_new.html', context)
    
    elif current_test.id != old_test.test.id:
        return  render(request, 'test/old_test.html', {'old_test':old_test,'current_test':current_test,})
    
    
@login_required(login_url='login') #Authentication   
def testsubmit(request):   

        json_data=json.loads(request.body.decode('utf-8'))    
        data = dict()
        current_user = request.user
        test_id=int(json_data[0]['testid'])  
        if Attempt.objects.filter(user=request.user,test=test_id).exists():
            data['attempted'] = "attempted"
            return JsonResponse(data)  
        test = Test.objects.get(id=test_id)     
        stime=On_Test.objects.get(user=request.user,test=test)           
        start_time=stime.started_time  
        end_time=datetime.now()
       

        if len(json_data)==1 and not 'questionid' in json_data[0]:
            
            Attempt.objects.create(user = current_user, test = test,score = 0,start_date_time=start_time,end_date_time=end_time)
            score=0
            On_Test.objects.filter(user=current_user,test=test).delete()     
        else:
            
            score = Attempt.Create(test_id,current_user,json_data,start_time) 
            
        
        data['score'] = score        
        return JsonResponse(data)
   
@complete_profile
@login_required(login_url='login') 
def view_result(request,test): 
    
    attempt=Attempt.objects.get(test=test,user=request.user)      
    question=Question.objects.filter(test__id=test)   
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")   
    return render(request, 'test/view_result.html', {'attempt':attempt,'question':question,'today':d1})

@complete_profile
@login_required(login_url='login') 
def view_answer(request,test):    
    attempt=Attempt.objects.get(test=test,user=request.user)      
    question=Question.objects.filter(test__id=test)      
    return render(request, 'test/view_answer.html', {'attempt':attempt,'question':question})

 
def delete_on_test(request,test):
    On_Test.objects.filter(user=request.user,test=test).delete()
    data = dict()
    data['status'] = 'done'       
    return JsonResponse(data)
   
@complete_profile
@login_required(login_url='login') 
def view_discussion(request,test): 
    if Attempt.objects.filter(test=test,user=request.user).exists():
        test=Test.objects.get(id=test)      
        return render(request, 'test/view_discussion.html', {'test':test,})

    else:
        return HttpResponse("Attend the test first")




@complete_profile
@login_required(login_url='login') 
def test_completed(request,test): 
    if Attempt.objects.filter(test=test,user=request.user).exists():
        test=Test.objects.get(id=test)      
        return render(request, 'test/test_completed.html', {'test':test,})

    else:
        return HttpResponse("Attend the test first")

@complete_profile
@login_required(login_url='login')
def load_question(request):
    data = dict()
    no = int(request.GET.get('question_no'))
    print(no)
    test = request.GET.get('test')
    if str(test) in request.session:
                
        #get test questions
        test_object=Test.objects.get(id=test)
        
        question = Question.objects.get(id=request.session[str(test)][no])
               
        context={
            
            'question' : question,
            'test':test_object,
            'question_no': no,
            
            
        }
        data['question'] = render_to_string('test/test_fly.html', context) 
        data['question_no'] = no
        data['question_id'] = question.id
        data['question_count'] = len(request.session[str(test)])
    else:
        data['error'] = "Something went Wrong"
    return JsonResponse(data)

def ajax_load_questions(request):
    data = dict()
    questions=request.GET.get('question')
    questions=request.GET.get('question')
    questions=json.loads(questions)
    questions = [x.strip() for x in questions.split(',')]
    questions=Question.objects.filter(id__in=questions)

    context={            
            'questions' : questions,      
            
        }
    data['questions'] = render_to_string('admin/question_fly.html', context) 

    return JsonResponse(data)