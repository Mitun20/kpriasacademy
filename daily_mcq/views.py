from django.shortcuts import render
from . models import Daily_Mcq
from mcq_test.models import Question,Test,Attempt, On_Test
from datetime import datetime
from django.db.models.functions import TruncMonth,TruncYear
from django.db.models import Count,Sum
import json
from django.http import JsonResponse,HttpResponse
from account.views import complete_profile


@complete_profile
def daily_mcq_list(request):
    today = datetime.now()   
    year=Test.objects.filter(daily_mcq__isnull=False,active=True).annotate(year=TruncYear('open_date')).values('year').annotate(total=Count('id')).order_by("year")[:5]
    test=Test.objects.filter(open_date__year=today.year,daily_mcq__isnull=False,active=True).annotate(month=TruncMonth('open_date')).values('month').annotate(total=Count('id')).order_by("month")
    return render(request, 'daily_mcq/view_daily_mcq_list.html', {'test':test,'year':year})


@complete_profile
def year_by_daily_mcq(request,year):
    today = datetime.now()   
    last_5_year=Test.objects.filter(daily_mcq__isnull=False,active=True).annotate(year=TruncYear('open_date')).values('year').annotate(total=Count('id')).order_by("year")[:5]
    test=Test.objects.filter(open_date__year=year,daily_mcq__isnull=False,active=True).annotate(month=TruncMonth('open_date')).values('month').annotate(total=Count('id')).order_by("month")
    return render(request, 'daily_mcq/view_daily_mcq_list.html', {'test':test,'year':last_5_year,})

@complete_profile
def daily_mcq_filter_by_month(request,month,year):   
    test=Test.objects.filter(open_date__month=month,open_date__year=year,daily_mcq__isnull=False,active=True).order_by('-open_date')
    print(test)
    return render(request, 'daily_mcq/view_month_wise_daily_mcq_list.html', {'test':test,'month':month})

@complete_profile
def test(request,test):
    if request.user.is_anonymous:
          test=Test.objects.get(id=test,daily_mcq__isnull=False)    
          questions=Question.objects.filter(test=test)    
          return render(request, 'daily_mcq/test.html', {'questions':questions,'test':test,})

    else:
        if not On_Test.objects.filter(user=request.user).exists():
            On_Test.objects.create(user=request.user,test_id=test,started_time=datetime.now())

        old_one=[]

        current_test=Test.objects.get(id=test,active=True)
        old_test=On_Test.objects.get(user=request.user)   
 
        if current_test.id == old_test.test.id:
            if Attempt.objects.filter(test=test,user=request.user).exists():
                return HttpResponse("No More attempts allowed")
        
            if not 'start_time_'+str(test) in request.session:
                request.session['start_time_'+str(test)]=datetime.now().strftime('%Y-%m-%d %H:%M:%S')        

            test=Test.objects.get(id=test,daily_mcq__isnull=False)    
            questions = test.question.all()
            questions_count=len(questions)
           
            return render(request, 'daily_mcq/test.html', {'questions':questions,'test':test,'questions_count':questions_count,})
        elif current_test.id != old_test.test.id:
            return  render(request, 'test/old_test.html', {'old_test':old_test,'current_test':current_test,})
    
@complete_profile
def mcqtestsubmit(request):       

        json_data=json.loads(request.body.decode('utf-8'))    
        data = dict()
        current_user = request.user

        test_id=int(json_data[0]['testid'])    
        test = Test.objects.get(id=test_id)        
        start_time=request.session['start_time_'+str(test_id)] 
        end_time=datetime.now()
       

        if len(json_data)==1 and not 'questionid' in json_data[0]:
            
            Attempt.objects.create(user = current_user, test = test,score = 0,start_date_time=start_time,end_date_time=end_time)
            score=0     
        else:
            
            score = Attempt.Mcq_Create(test_id,current_user,json_data,start_time)    
        #del request.session['start_time_'+str(test_id)]
        
        data['score'] = score
        request.session['mark'] = score[0]        
        request.session['negative_mark'] = score[1]
        return JsonResponse(data)
  
@complete_profile
def daily_mcq_answer(request,test):
    if not  request.user.is_anonymous:
        attempt=Attempt.objects.get(test=test,user=request.user)    
        question=Question.objects.filter(test=test)      
        return render(request, 'daily_mcq/reg_user_view_answer.html', {'question':question,'attempt':attempt})
    else:
        if 'negative_mark' in request.session:
            negative_mark = request.session['negative_mark']
            
            mark = request.session['mark']

        test=Test.objects.get(id=test)    
        question=Question.objects.filter(test=test)              
        return render(request, 'daily_mcq/view_answer.html', {'question':question,'test':test,'negative_mark':negative_mark,'mark':mark})