from django.shortcuts import render
from . models import Series
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta
from account.models import Test_Series_Enrolment
from mcq_test.models import Attempt, Test,Response,Option
from django.http import HttpResponse, JsonResponse
from django.db.models import Max, Count,Min,Avg
from assignment.models import Assignment,Submission,AFile
from django.shortcuts import redirect
from subject.models import Subject
from account.views import complete_profile
# Create your views here.

@complete_profile
@login_required(login_url='login')
def test_series_list(request):       
    series=Series.objects.filter(start_date__lte=date.today(), end_date__gte=date.today(),active=True).order_by('-start_date')       
    return render(request, 'test_series/test_series_list.html', {'series':series,})

@complete_profile
@login_required(login_url='login')
def my_test_series_list(request):      
    series=Series.objects.filter(test_series_enrolment__user=request.user,start_date__lte=date.today(), end_date__gte=date.today(),active=True).order_by('-start_date')       
    return render(request, 'test/test_series_list.html', {'series':series,})

@complete_profile
@login_required(login_url='login')
def series_performance(request,pk):
    
    if Test_Series_Enrolment.objects.filter(series__id=pk,user=request.user).exists():
        test=Test.objects.filter(test_series=pk,active=True).order_by('open_date')
        subjects=Test.objects.filter(test_series=pk).values_list('question__subject', flat=True).distinct().order_by('open_date')

        subject_name = list()
        total_questions= list()
        attempted_question= list()
        correct_ans = list()
        incorrect_ans = list()
        marks= list()

        subjects=Subject.objects.filter(id__in=subjects)

        for subject in subjects:
            subject_name.append(subject.name)          
            q_count=Test.objects.filter(question__subject=subject.id,test_series=pk).aggregate(count_question=Count('question'))
            
            total_questions.append(q_count['count_question'])
            responses = Response.objects.filter(option__question__subject=subject,attempt__test__test_series=pk,attempt__user=request.user,attempt__test__in=test)

            attempted_question.append(len(responses))
            attempted= 0
            correct= 0
            incorrect = 0
            mark=0
            
            for response in responses:
                attempted=attempted+1

                if response.option.value > 0:
                    correct+=1 
                else:
                   
                    incorrect+=1 
                
                   
                if response.option.value > 0:
                    positive_mark=Option.objects.get(id=response.option.id)
                    mark+=positive_mark.question.mark
                     
            
            correct_ans.append(correct)
            incorrect_ans.append(incorrect)
            marks.append(round(mark,2))
           
          
     

        #Attempted Progress in a Module

        test_names = list()
        attempted_pm=list()
        correct_pm=list()
        incorrect_pm=list()

        #your score compare with topper
        your_score = list()
        topper = list()
        median = list()

        count=1
        test_without_csat=Test.objects.filter(test_series=pk,active=True).order_by('open_date').exclude(name__icontains = 'csat')
        for test_pm in test_without_csat:
            #Attempted Progress in a Module
            test_names.append(test_pm.name)
            responses=Response.objects.filter(attempt__test=test_pm,attempt__user=request.user)
            
            correct=0
            incorrect=0
            attempted=0

            for response in responses:
                attempted+=response.option.question.mark

                
                if response.option.value > 0:
                    correct+=response.option.value

                else:                   
                    incorrect+=response.option.question.mark
                

            attempted_pm.append(attempted)
            correct_pm.append(correct)
            incorrect_pm.append(round(incorrect,2))

            #your score compare with topper
            data = Test.objects.filter(id=test_pm.id).aggregate(max_score=Max('attempt__score'),avg_score=Avg('attempt__score'))
            if data['max_score'] != None:
                topper.append(round(data['max_score'],2))
            else:
                topper.append(0)

            #min score           
            if data['avg_score'] != None:
                median.append(round(data['avg_score'],2))
            else:
                median.append(0)
            try:
                attempt=Attempt.objects.get(test__id=test_pm.id,user=request.user)
                your_score.append(attempt.score)

            except:
                 your_score.append(0)


            if count == 1:
                series=Test.objects.get(id=test_pm.id)
                series_name=series.test_series

            else:
                pass

            count+=count
      


        
        context =      {
            'subject_names' : subject_name,
            'total_questions' : total_questions,
            'attempted_questions' : attempted_question,
            'correct_ans' : correct_ans,
            'incorrect_ans' : incorrect_ans,
            'marks': marks,
            'tests'  : test,
            'subjects':subjects,
            'test_names' :test_names ,
            'attempted_pm' :attempted_pm,
            'correct_pm': correct_pm,
            'incorrect_pm' :incorrect_pm,
            'topper' :topper,
            'median' : median,
            'your_score': your_score,
            'series_name':series_name,
            'test_without_csat':test_without_csat,
          }


        return render(request,'test/performance.html',context)


    else:
        return HttpResponse('You are not allowed to view this page.')

  

@login_required
def ajax_load_test(request):
    series_id=request.GET.get('series_id')
    test_id=request.GET.get('test')
    data = dict()

    
    if Test_Series_Enrolment.objects.filter(series__id=series_id,user=request.user).exists():
       
        test=Test.objects.filter(id=test_id)
        subjects=Test.objects.filter(id=test_id).values_list('question__subject', flat=True).distinct()
        temp_1="hai"
        subject_name = list()
        total_questions= list()
        attempted_question= list()
        correct_ans = list()
        incorrect_ans = list()
        marks= list()

        subjects=Subject.objects.filter(id__in=subjects)
        
        for subject in subjects:
            subject_name.append(subject.name)
            
            
            q_count=Test.objects.filter(id=test_id,question__subject=subject.id,test_series=series_id).aggregate(count_question=Count('question'))
            
            total_questions.append(q_count['count_question'])
            responses = Response.objects.filter(option__question__subject=subject,attempt__test__test_series=series_id,attempt__user=request.user,attempt__test=test_id)

            attempted_question.append(len(responses))
            attempted= 0
            correct= 0
            incorrect = 0
            mark=0
            
            for response in responses:
                attempted=attempted+1

                if response.option.value > 0:
                    correct+=1 
                else:
                   
                    incorrect+=1 
                
                   
                if response.option.value > 0:
                    positive_mark=Option.objects.get(id=response.option.id)
                    mark+=positive_mark.question.mark
                     
            
            correct_ans.append(correct)
            incorrect_ans.append(incorrect)
            marks.append(round(mark,2))
           
          

        
        data['subject_names']=subject_name
        data['total_questions']=total_questions
        data['attempted_questions'] = attempted_question
        data['correct_ans'] = correct_ans
        data['incorrect_ans'] = incorrect_ans
        data['marks'] = marks
        data['temp1'] = temp_1
        
        return JsonResponse(data) 


    else:
        data['marks'] = "not allowed"
        
        return JsonResponse(data)


@login_required
def ajax_load_ysc_test(request):
    
    series_id=request.GET.get('series_id')
    test_id=request.GET.get('test')
    data=dict()
    

    
    #your score compare with topper
    your_score = list()
    topper = list()
    median = list()
    test_names= list()

    test = Test.objects.get(id=test_id)
    
    test_names.append(test.name)


    #your score compare with topper
    data = Test.objects.filter(id=test.id).aggregate(max_score=Max('attempt__score'),avg_score=Avg('attempt__score'))
    if data['max_score'] != None:
        topper.append(round(data['max_score'],2))
    else:
        topper.append(0)

    #min score           
    if data['avg_score'] != None:
        median.append(round(data['avg_score'],2))
    else:
        median.append(0)
    
    try:
        attempt=Attempt.objects.get(test__id=test.id,user=request.user)
        your_score.append(attempt.score)

    except:
        your_score.append(0)
      


    data['test_name']=test_names
    data['topper']=topper
    data['median'] = median
    data['your_score'] = your_score
        
    return JsonResponse(data) 


  

@login_required
def ajax_load_pm_test(request):
    
    series_id=request.GET.get('series_id')
    test_id=request.GET.get('test')
    data=dict()
    

    test_names = list()
    attempted_pm=list()
    correct_pm=list()
    incorrect_pm=list()

    test = Test.objects.get(id=test_id)
    
    test_names.append(test.name)
    responses=Response.objects.filter(attempt__test=test,attempt__user=request.user)
            
    correct=0
    incorrect=0
    attempted=0

    for response in responses:
        attempted+=response.option.question.mark

                
        if response.option.value > 0:
            correct+=response.option.value

        else:                   
            incorrect+=response.option.question.mark
                

    attempted_pm.append(attempted)
    correct_pm.append(correct)
    incorrect_pm.append(incorrect)
   


    data['test_name']=test_names
    data['attempted_pm']=attempted_pm
    data['correct_pm'] = correct_pm
    data['incorrect_pm'] = incorrect_pm

        
    return JsonResponse(data) 


@login_required
def ajax_load_mpm_test(request):
    series_id=request.GET.get('series_id')
    test_id=request.GET.get('test')

    data=dict()   

    test_names = list()
    mark=list()
    test = Test.objects.get(id=test_id)
    try:
        attempt=Attempt.objects.get(user=request.user,test=test)
        mark.append(attempt.score)

    except:
        mark.append('0')
  
    test_names.append(test.name)
    data['test_name']=test_names 
    data['mark']=mark
    return JsonResponse(data) 

  



@login_required
def ajax_load_subject(request):
    series_id=request.GET.get('series_id')
    subject=request.GET.get('subject')
    

    data = dict()
    
    if Test_Series_Enrolment.objects.filter(series__id=series_id,user=request.user).exists():
       
        test=Test.objects.filter(test_series=series_id)
        subjects=Test.objects.filter(test_series=series_id,question__subject=subject).values_list('question__subject', flat=True).distinct()

        subject_name = list()
        total_questions= list()
        attempted_question= list()
        correct_ans = list()
        incorrect_ans = list()
        marks= list()

        subjects=Subject.objects.filter(id__in=subjects)

        for subject in subjects:
            subject_name.append(subject.name)          
            q_count=Test.objects.filter(question__subject=subject.id,test_series=series_id).aggregate(count_question=Count('question'))
            
            total_questions.append(q_count['count_question'])
            responses = Response.objects.filter(option__question__subject=subject,attempt__test__test_series=series_id,attempt__user=request.user,attempt__test__in=test)

            attempted_question.append(len(responses))
            attempted= 0
            correct= 0
            incorrect = 0
            mark=0
            
            for response in responses:
                attempted=attempted+1

                if response.option.value > 0:
                    correct+=1 
                else:
                   
                    incorrect+=1 
                
                   
                if response.option.value > 0:
                    positive_mark=Option.objects.get(id=response.option.id)
                    mark+=positive_mark.question.mark
                     
            
            correct_ans.append(correct)
            incorrect_ans.append(incorrect)
            marks.append(round(mark,2))
          


        data['subject_names']=subject_name
        data['total_questions']=total_questions
        data['attempted_questions'] = attempted_question
        data['correct_ans'] = correct_ans
        data['incorrect_ans'] = incorrect_ans
        data['marks'] = marks
        
        return JsonResponse(data) 


    else:
        return HttpResponse('You are not allowed to view this page.')

  

def test_series_assignment(request,pk):
    assignment=Assignment.objects.filter(test_series=pk)
    return render(request,'assignment.html',{'assignments':assignment,})

@complete_profile
@login_required(login_url='login')
def assignment(request,assignment_id):
    if request.method == 'POST':    
        form = SubmissionForm(request.POST)
        sfileform = SForm(request.POST, request.FILES)
        submission=Submission.objects.filter(assignment_id=assignment_id,student=request.user)
        if not submission:
            if form.is_valid() and sfileform.is_valid():
                submission = form.save(commit=False)
                submission.assignment_id=assignment_id
                submission.student=request.user
                submission.marks=0
                submission = form.save()
                sfile = sfileform.save(commit=False)
                sfile.submission=submission
                sfile=sfileform.save()
            
            return redirect('/')
        else:
            return redirect('/')

 
    else:        
        if Submission.objects.filter(assignment_id=assignment_id,student=request.user):            
            assignment=None
        else:
            assignment=Assignment.objects.get(id=assignment_id)
        
        afile=AFile.objects.filter(assignment=assignment) 
        form = SubmissionForm()
        sfileform = SForm()
        return render(request, 'view_assignment.html', {'assignment':assignment,'afiles':afile,'form':form,'sfileform':sfileform,}) 


@complete_profile
@login_required(login_url='login')
def test_rank(request,test):       
    if Attempt.objects.filter(test=test,user=request.user).exists():
        attempt=Attempt.objects.filter(test=test).order_by('-score')
        return render(request, 'test_series/rank.html', {'attempt':attempt,})




#Csat Attempted Progress Module

@login_required
def ajax_load_apm_csat_test(request):
    
    series_id=request.GET.get('series_id')
    test=Test.objects.filter(test_series=series_id,name__icontains = 'csat',active=True).order_by('open_date')
    data= dict()
    test_names = list()
    attempted_pm=list()
    correct_pm=list()
    incorrect_pm=list()


    count=1
    for test_pm in test:
        #Attempted Progress in a Module
        test_names.append(test_pm.name)
        responses=Response.objects.filter(attempt__test=test_pm,attempt__user=request.user)
            
        correct=0
        incorrect=0
        attempted=0

        for response in responses:
            attempted+=response.option.question.mark

                
            if response.option.value > 0:
                correct+=response.option.value

            else:                   
                incorrect+=response.option.question.mark
                

        attempted_pm.append(attempted)
        correct_pm.append(correct)
        incorrect_pm.append(incorrect)



    data['test_name']=test_names
    data['attempted_pm']=attempted_pm
    data['correct_pm'] = correct_pm
    data['incorrect_pm'] = incorrect_pm
        
    return JsonResponse(data) 


  




#Csat Marks Progress Module

@login_required
def ajax_load_mpm_csat_test(request):
    
    series_id=request.GET.get('series_id')
    test=Test.objects.filter(test_series=series_id,name__icontains = 'csat',active=True).order_by('open_date')
    data= dict()
    test_names = list()
    score= list()


    for test_pm in test:
        #Attempted Progress in a Module
        test_names.append(test_pm.name)
        try:
            attempt=Attempt.objects.get(test=test_pm,user=request.user)
            score.append(attempt.score)
        except:
            score.append('0')


    data['test_name']=test_names
    data['score']=score

    return JsonResponse(data) 




@login_required
def ajax_load_cwt_csat_test(request):
    
    series_id=request.GET.get('series_id')

    data=dict()
    
    #your score compare with topper
    your_score = list()
    topper = list()
    median = list()

    test_names= list()

    tests=Test.objects.filter(test_series=series_id,active=True,name__icontains = 'csat').order_by('open_date')
    
    for test in tests:
        test_names.append(test.name)
        #your score compare with topper
        data = Test.objects.filter(id=test.id).aggregate(max_score=Max('attempt__score'),avg_score=Avg('attempt__score'))
        if data['max_score'] != None:
            topper.append(round(data['max_score'],2))
        else:
            topper.append(0)

        #min score           
        if data['avg_score'] != None:
            median.append(round(data['avg_score'],2))
        else:
            median.append(0)
    
        try:
            attempt=Attempt.objects.get(test__id=test.id,user=request.user)
            your_score.append(attempt.score)
        except:
            your_score.append(0)
      

    data['test_names']=test_names
    data['topper']=topper
    data['median'] = median
    data['your_score'] = your_score
        
    return JsonResponse(data)