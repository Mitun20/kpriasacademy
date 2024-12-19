from django.shortcuts import render,redirect
from .models import Course,Part,Topic,Video,Live_Sessions
from datetime import datetime, date
from account.models import Course_Enrolment
from django.http import HttpResponse,JsonResponse
from mcq_test.models import Test,Attempt,On_Test,Response
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mcq_test.models import Question,Attempt
from assignment.models import Assignment
from .forms import SubmissionForm
from assignment.models import Submission,AFile
from django.template.loader import render_to_string
from account.views import complete_profile

# Create your views here.

@complete_profile
@login_required(login_url='login') 
def course_list(request):  
    course=Course.objects.filter(open_date__lte=datetime.today(), close_date__gte=datetime.today(),active=True).order_by('open_date')  
    return render(request, 'course/course_list.html', {'course':course,})

@complete_profile
@login_required(login_url='login') 
def my_course_list(request):  
    course=Course.objects.filter(course_enrolment__user=request.user,open_date__lte=datetime.today(), close_date__gte=datetime.today(),active=True).order_by('open_date')  
    return render(request, 'course/course_list.html', {'course':course,})

@complete_profile
@login_required(login_url='login') 
def course_detail(request,course):
    if not  Course_Enrolment.objects.filter(course=course,user=request.user).exists():
        return HttpResponse("You don't have rights to access the Course detail page")
        
    part=Part.objects.filter(course=course)
    return render(request, 'course/part_list.html', {'part':part,})


@complete_profile
@login_required(login_url='login') 
def material(request,part):
    if not  Course_Enrolment.objects.filter(course__part=part,user=request.user).exists():
        return HttpResponse("You don't have rights to access the materials")
        
    topic=Topic.objects.filter(part=part)    
    return render(request, 'course/material.html', {'topics':topic,'part':part})


@complete_profile
@login_required(login_url='login') 
def video(request,part):
    if not  Course_Enrolment.objects.filter(course__part=part,user=request.user).exists():
        return HttpResponse("You don't have rights to access the videos")
        
    topic=Topic.objects.filter(part=part).order_by('id')    
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    
    return render(request, 'course/video.html', {'topics':topic,'part':part, 'today':d1})



@complete_profile
@login_required(login_url='login') 
def session(request,part,course):
    if not  Course_Enrolment.objects.filter(course__part=part,user=request.user).exists():
        return HttpResponse("You don't have rights to access the sessions")
        

    course_enrolment=Course_Enrolment.objects.get(user=request.user,course_id=course)
    session=Live_Sessions.objects.filter(batch=course_enrolment.batch,topic__part=part,end_date_time__gte=datetime.today()).order_by('start_date_time')
    return render(request, 'course/session.html', {'sessions':session,'part':part})


@complete_profile
@login_required(login_url='login') 
def test_list(request,part):    
    test= Test.objects.filter(course_part=part,active="True").order_by('open_date') 
    return render(request, 'course/view_test_list.html', {'test':test,})



@complete_profile
@login_required(login_url='login') 
def test(request,test):
    if Attempt.objects.filter(test=test,user=request.user).exists():
        return HttpResponse("No More attempts allowed")

    if not 'start_time_'+str(test) in request.session:
        request.session['start_time_'+str(test)]=datetime.now().strftime('%Y-%m-%d %H:%M:%S') 

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


        test_object=Test.objects.get(id=test,course_part__isnull=False)
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
        return render(request, 'course/test.html', context)
    
    elif current_test.id != old_test.test.id:
        return  render(request, 'test/old_test.html', {'old_test':old_test,'current_test':current_test,})
    

@complete_profile
@login_required(login_url='login') 
def view_result(request,test): 
    
    attempt=Attempt.objects.get(test=test,user=request.user)      
    question=Question.objects.filter(test__id=test)      
    return render(request, 'course/view_result.html', {'attempt':attempt,'question':question})


@complete_profile
@login_required(login_url='login') 
def view_answer(request,test):    
    attempt=Attempt.objects.get(test=test,user=request.user)      
    question=Question.objects.filter(test__id=test)      
    return render(request, 'course/view_answer.html', {'attempt':attempt,'question':question})


#mains test start

@complete_profile
@login_required(login_url='login') 
def course_mains_test(request):  
    course=Course.objects.filter(open_date__lte=datetime.today(), close_date__gte=datetime.today(),active=True).order_by('open_date')  
    return render(request, 'course/course_mains_test.html', {'course':course,})


@complete_profile
@login_required(login_url='login')
def course_mains_part_test(request,part):      
    if  Course_Enrolment.objects.filter(course__part=part,user=request.user).exists() or request.user.groups.filter(name='Instructor').exists():
        #course=Course.objects.get(id=course)
        part=Part.objects.filter(id=part)
        assignments=Assignment.objects.filter(part__in=part) 
        
        return render(request, 'course/course_mains_test_detail.html', {'assignments':assignments,})

    return HttpResponse("You don't have rights to access the test series")




@complete_profile
@login_required(login_url='login')
def course_mains_test(request,assignment_id):
    if not Course_Enrolment.objects.filter(course__part__assignment=assignment_id,user=request.user).exists():
        return HttpResponse("You don't have rights to access the test series")
    if request.method == 'POST':    
        form = SubmissionForm(request.POST, request.FILES)  
        submission=Submission.objects.filter(assignment_id=assignment_id,user=request.user)
        if not submission:
            if form.is_valid():
                submission = form.save(commit=False)
                submission.assignment_id=assignment_id
                submission.user=request.user
                submission.marks=0
                submission.status='S'
                submission = form.save()
              

            
            return redirect('course_mains_part_test', part=submission.assignment.part.id)
        else:
            return redirect('course/')

 
    else:        
        if Submission.objects.filter(assignment_id=assignment_id,user=request.user):            
            assignment=None
        else:
            assignment=Assignment.objects.get(id=assignment_id,)
        
        afile=AFile.objects.get(assignment=assignment) 
        form = SubmissionForm()

        return render(request, 'course/view_assignment.html', {'assignment':assignment,'afile':afile,'form':form,}) 

@complete_profile
@login_required(login_url='login')
def course_mains_test_result(request,assignment_id):

    if  Submission.objects.filter(user=request.user,status='A',assignment=assignment_id).exists():
        submission=Submission.objects.get(user=request.user,assignment=assignment_id)
        return render(request, 'course/view_mains_test_result.html', {'submission':submission}) 


@complete_profile
@login_required(login_url='login')
def load_question(request):
    data = dict()
    no = int(request.GET.get('question_no'))
    test = request.GET.get('test')

          
    #get test questions
    test_object=Test.objects.get(id=test)
    questions=test_object.question.all()
        
    question = test_object.question.all()[no]
               
    context={
            
        'question' : question,
        'test':test_object,
        'question_no':no
            
            
        }
    data['question'] = render_to_string('test/test_fly.html', context) 
    data['question_no'] = no
    data['question_id'] = question.id
    data['question_count'] = len(questions)
  
    return JsonResponse(data)


@complete_profile
@login_required(login_url='login')
def course_performance(request,pk):

    if  Course_Enrolment.objects.filter(course__id=pk,user=request.user).exists():
        #Attempted Progress in a Module

        test_names = list()
        score = list ()
    


        tests = Test.objects.filter(course_part__course=pk).order_by('open_date')
        for test in tests:
            #Attempted Progress in a Module
            test_names.append(test.name)
            try:
                mark=Attempt.objects.get(test=test,user=request.user)
                score.append(mark.score)
                
            except:
               
                score.append(0)

            


        
        context =      {
            'test_names' : test_names,
            'score' : score,
      
          }

        return render(request,'course/performance.html',context)

          




    else:
        return HttpResponse('You are not allowed to view this page.')
        
        
        
@complete_profile        
@login_required(login_url='login') 
def schedule(request,course_id):


    if not Course_Enrolment.objects.filter(course=course_id,user=request.user).exists():
        return HttpResponse("You don't have rights to access the test series")

    else:
        course=Course_Enrolment.objects.get(user=request.user,course=course_id)
        schedules=Live_Sessions.objects.filter(batch=course.batch,topic__part__course=course_id,end_date_time__gte=datetime.today()).order_by('start_date_time')   
        return render(request, 'course/view_schedule.html', {'schedules':schedules,})