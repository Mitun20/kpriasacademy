from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import CustomAuthForm,EditUserForm,SignupForm, EducationFormSet, FamilyFormSet
from .models import Test_Series_Enrolment,User,Course_Enrolment,Mains_Test_Series_Enrolment, Miscellaneous_Fee, Enquiry
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from course.models import Course,Batch
from tseries.models import Series
from datetime import datetime, date
from daily_mcq.models import Daily_Mcq
from mcq_test.models import Test,Attempt
from django.contrib.auth.hashers import make_password
from django.db.models import Q, Max, Min, Avg
from django.http import JsonResponse, HttpResponse
from itertools import chain
import openpyxl
from mcq_test.models import Question,Option
import math
import re
from subject.models import Subject
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm 
from scholarship.models import Scholarship_Test
from mains_test_series.models import Mains_Test_Series
import random
import json
from .serializers import EnrollmentSerializer
from django.conf import settings 
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer
from django.core.mail import send_mail
from functools import wraps
from django.http import HttpResponseRedirect
from datetime import date

# Create your views here.
def complete_profile(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):      
      if User.objects.filter(Q(test_series_enrolment__user=request.user) | Q(course_enrolment__user=request.user) | Q(mains_test_series_enrolment__user=request.user)):
          try:
              profile = User.objects.get(username=request.user,community__isnull=False,religion__isnull=False,mother_tongue__isnull=False,first_name__isnull=False,last_name__isnull=False,mobile_no__isnull=False,age__isnull=False)
          except:
              return redirect('/edit_profile/')

          if profile.profile_picture and profile.signature_of_the_applicant: 
              if Course_Enrolment.objects.filter(user=request.user,batch__isnull=True).exists():
                  return redirect('/batch_update/')
              else:
                  return function(request, *args, **kwargs)
          else:
              return redirect('/edit_profile/')              
              
      else:
          return function(request, *args, **kwargs)

  return wrap


class EnrollmentView(APIView):
    def post(self,request,format=None):
        payload = json.dumps(request.data)
        payload = json.loads(payload)

        try:
            user=User.objects.get(username=payload['email'])
        
        except User.DoesNotExist:
            password= random.randint(1000,9999)                    
            hashed_password = make_password(str(password))
            user= User(username=payload['email'],first_name=payload['name'],email=payload['email'],password=hashed_password)
            user.save()
            #send mail
            website='http://kpr.us.tempcloudsite.com/'
            email=payload['email']
        
            subject = 'KPR IAS Academy Portal'
            message = 'Login Crendentials: \n username: {} \n and password: {} \n website: {}'.format(email,password,website)
        
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [payload['email'] , ] 
            send_mail( subject, message, email_from, recipient_list )

        try:
            content_name = payload['content_name']
            if content_name and not Miscellaneous_Fee.objects.filter(user=user,paid_for=content_name,amount=payload['amount']).exists():
                miscellaneous_fee = Miscellaneous_Fee.objects.create(user=user,paid_for=content_name,amount=payload['amount'])
                miscellaneous_fee.save()
                return Response("Success", status=status.HTTP_201_CREATED)
            else:
                return Response("Success", status=status.HTTP_201_CREATED)

        except:
            pass
        try:
            course = Course.objects.get(title=payload['content'])
            if not Course_Enrolment.objects.filter(user__email=payload['email'],course__title=payload['content']).exists():
                course_enrolment = Course_Enrolment.objects.create(course=course,user=user,joined_on=datetime.now())
                course_enrolment.save()
                return Response("Success", status=status.HTTP_201_CREATED)
            else:
                return Response("Success", status=status.HTTP_201_CREATED)

        except Course.DoesNotExist:
            try:
                series = Series.objects.get(title=payload['content'])

                if not Test_Series_Enrolment.objects.filter(user__email=payload['email'],series__title=payload['content']).exists():
                    prelims_enrolment = Test_Series_Enrolment.objects.create(series=series,user=user,joined_on=datetime.now())
                    prelims_enrolment.save()
                    serializer = EnrollmentSerializer(user.email,series.title)
                    return Response("Success", status=status.HTTP_201_CREATED)
                else:
                    return Response("Success", status=status.HTTP_201_CREATED)
            except Series.DoesNotExist:
                try:
                    mains = Mains_Test_Series.objects.get(title=payload['content'])
                    if not Mains_Test_Series_Enrolment.objects.filter(user__email=payload['email'],series__title=payload['content']).exists():
                        mains_enrolment = Mains_Test_Series_Enrolment.objects.create(series=mains,user=user,joined_on=datetime.now())
                        mains_enrolment.save()
                        serializer = EnrollmentSerializer(user.email,mains.title)
                        return Response("Success", status=status.HTTP_201_CREATED)
                    else:
                        return Response("Success", status=status.HTTP_201_CREATED)

                except Mains_Test_Series.DoesNotExist:
                    return JsonResponse({'error': 'Something terrible went wrong,contact your adminstrator.'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# Create your views here.
class CustomLoginView(LoginView):
    authentication_form = CustomAuthForm
    redirect_authenticated_user = True
    


'''def handle(self, *args, **options):
    if not User.objects.filter(username='myuser').exists():
        User.objects.create_superuser('myuser','myuser@myemail.com','mypassword')
    return redirect('/')'''

#logout
def logout(request):
    request.session['is_logout'] = True
    user_logout(request)

    return render(request,'account/logout.html', {})


def course_enrolment_batch_update(request,course_enrolment_id):
    if request.method == 'POST':
        batch=request.POST.get('batch')
        Course_Enrolment.objects.filter(id=course_enrolment_id).update(batch_id=batch)
        return redirect('edit_profile')
        
@login_required(login_url='login') 
def edit_profile(request):
    
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        form = EditUserForm(request.POST or None, request.FILES or None, instance=user)
     
        try:
            education_form = EducationFormSet(request.POST or None, request.FILES or None ,instance=user)
            family_form=FamilyFormSet(request.POST or None ,instance=user)
        except:
            education_form = EducationFormSet(request.POST , request.FILES )
            family_form=FamilyFormSet(request.POST )
        

        if form.is_valid() and education_form.is_valid() and family_form.is_valid():
            form=form.save(commit=False)
            form.once_submited=True
            form.save()
            education_form.save()
            family_form.save()

            return redirect('/')
        else:     

            return render(request,'account/edit_profile.html', {'form': form,'education_form':education_form,'family_form':family_form,})



    else:
        
        
        user=User.objects.get(username=request.user)
        if user.once_submited:
            return redirect('view_profile')
            
        form = EditUserForm(instance=user)       

        try:
            education_form=EducationFormSet(instance=user)
            family_form=FamilyFormSet(instance=user)
        except:
            education_form=EducationFormSet()
            family_form=FamilyFormSet(instance=user)

                    

        return render(request,'account/edit_profile.html', {'form': form,'education_form':education_form,'family_form':family_form,})
    
    return render(request, 'account/edit_profile.html')

def change_password(request):     
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_default_password=False
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form
    })




@complete_profile
@login_required(login_url='login') 
def home(request):

    enrolled_serieses=Series.objects.filter(start_date__lte=date.today(), end_date__gte=date.today(),active=True,test_series_enrolment__user=request.user).order_by('start_date')
    serieses=Series.objects.filter(start_date__lte=date.today(), end_date__gte=date.today(),active=True).order_by('start_date').exclude(id__in=enrolled_serieses)
    daily_mcq=Test.objects.filter(daily_mcq__isnull=False,active=True).order_by('-open_date')[:3]
    enrolled_courses=Course.objects.filter(course_enrolment__user=request.user,open_date__lte=datetime.today(), close_date__gte=datetime.today(),active=True).order_by('open_date') 
    courses=Course.objects.filter(open_date__lte=datetime.today(), close_date__gte=datetime.today(),active=True).exclude(id__in=enrolled_courses)
    enrolled_mains_tests=Mains_Test_Series.objects.filter(start_date__lte=date.today(), end_date__gte=date.today(),active=True,mains_test_series_enrolment__user=request.user).order_by('start_date')
    mains_tests=Mains_Test_Series.objects.filter(start_date__lte=date.today(), end_date__gte=date.today()).order_by('start_date').exclude(id__in=enrolled_mains_tests)
    return render(request, 'home.html', {'enrolled_courses':enrolled_courses,'courses':courses,'enrolled_serieses':enrolled_serieses,'serieses':serieses,'daily_mcq':daily_mcq,'enrolled_mains_tests':enrolled_mains_tests,'mains_tests':mains_tests,})



@complete_profile
@login_required(login_url='login') 
def dashboard(request):     
    test_series=Series.objects.filter(test_series_enrolment__user=request.user,start_date__lte=date.today(), end_date__gte=date.today(),active=True).order_by('-start_date')       
    return render(request, 'dashboard.html', {'test_series':test_series,})


def dashboard_home(request):
    if request.user.is_superuser:
        series=Series.objects.filter(active=True)       

    elif request.user.groups.filter(name='Instructor').exists():
        series=Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)
        
    return render(request, 'dashboard/home.html', {'series':series,})

@complete_profile
def test_series_dashboard(request,series_id):
    if Test_Series_Enrolment.objects.filter(series__id=series_id).exists():
        test_names = list()        
        max_scores = list()
        low_scores=list()
        avg_scores=list()
        
        student=User.objects.filter(test_series_enrolment__series=series_id)
        
        
        tests = Test.objects.filter(test_series__id=series_id).order_by('open_date')
        
        for test in tests:
            test_names.append(test.name)
            data = Test.objects.filter(id=test.id).aggregate(max_score=Max('attempt__score'),low_score=Min('attempt__score'),avg_score=Avg('attempt__score'))
            if data['max_score'] != None:
                max_scores.append(data['max_score'])
            else:
                max_scores.append(0)

            #min score           
            if data['low_score'] != None:
                low_scores.append(data['low_score'])
            else:
                low_scores.append(0)

            #avg score           
            if data['avg_score'] != None:
                avg_scores.append(round(data['avg_score'],2))
            else:
                avg_scores.append(0)

        
        context =      {
            'test_names' : tests,           
            'tests' : test_names,            
            'max_scores' : max_scores,
            'low_scores'  : low_scores,
            'avg_scores'  : avg_scores,
            'students'   : student,
            
            
        }
     

        return render(request,'dashboard/performance.html',context)
        
    else:
        return HttpResponse('You are not allowed to view this page.')


@login_required
def draw_dashboard(request):
    data = dict()
    user = request.GET.get('user')
    series_id=request.GET.get('series_id')
    scores = list()
    score_for_table=list()
    test_names=[]
    negative_score=[]

    tests = Test.objects.filter(test_series__id=series_id).order_by('open_date')
    for test in tests:
        test_names.append(test.name)
        
        if Attempt.objects.filter(test=test,user=user).exists():
            attempt = Attempt.objects.get(test=test,user=user)
            scores.append(attempt.score)
        
            negative_score.append(attempt.nagative_marks())
        else:
            scores.append("Not Attempted")
            negative_score.append("Not Attempted")
            



    
    data['test_names']=test_names
    data['scores']=scores
    data['negative_score'] = negative_score
  

    return JsonResponse(data) 



@login_required
def draw_dashboard_test(request):
    
    data = dict()
    test = request.GET.get('test')
    series_id=request.GET.get('series_id')
    scores=list()
    student_names=[]
    attempts=[]
    testname=[]
    negative_score=list()


    students=User.objects.filter(test_series_enrolment__series=series_id,attempt__test=test).order_by('-attempt__score').distinct()
    not_attempted_user=User.objects.filter(test_series_enrolment__series=series_id).exclude(id__in=students)
    test_name = Test.objects.get(id=test)
    students = list(chain(students, not_attempted_user))
   
   
    for student in students:
        student_names.append(student.first_name)
        
        if Attempt.objects.filter(test=test,user=student).exists():
            attempt = Attempt.objects.get(user=student,test=test)
            scores.append(attempt.score)            
            negative_score.append(attempt.nagative_marks())
            
        else:          
            scores.append("Not Attempted")
            negative_score.append("Not Attempted")
            


    
    data['student']=student_names
    data['scores']=scores
    data['testname']=test_name.name
    data['negative_score']=negative_score
    
    return JsonResponse(data) 


@login_required(login_url='login')
def question_upload(request):
    if request.user.groups.filter(name='Instructor').exists():
        if "GET" == request.method:
            series=Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))
            courses= Course.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))
            daily_mcq_tests=Test.objects.filter(daily_mcq__isnull=False,created_by=request.user,open_date__gt=date.today())
            scholarship=Scholarship_Test.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))
            
            
            context =      {
                'series' : series,
                'courses': courses,
                'daily_mcq_tests'   : daily_mcq_tests,
                'scholarship' : scholarship,

                }

            return render(request, 'quest.html', context)
        else:
            excel_file = request.FILES["excel_file"]
            try:
                test_ID =  request.POST['testie']
            except:
                test_ID=[]

            test_type= request.POST['test_type'] 
         
            error_rows=[]
  
           # you may put validations here to check extension or file size

            wb = openpyxl.load_workbook(excel_file)

            # getting a particular sheet by name out of many sheets
            worksheet = wb["Sheet1"]
 
            excel_data = list()
            # iterating over the rows and
            # getting value from each cell in row
            d=0
            for count, row in enumerate(worksheet.iter_rows()):                
                if count == 0:
                    continue
                elif row[0].value == 'end':
                    break

                question_description=str(row[1].value).replace('\n','<br>')
                answer_description = str(row[2].value).replace('\n','<br>')
                
                row_data = list()
                
                try:
                    if  str(str(row[0].value)) !="None" and question_description != "None" and answer_description != "None" and str(row[4].value) != "None" and str(row[9].value) != "None" and int(row[9].value) <= 4:
                        subject=Subject.objects.get(name__exact=row[3].value)
                
                        q = Question(name=str(row[0].value),description=question_description,answer_description=answer_description,subject=subject,mark=row[4].value)
                        q.save()

                        for  i in range(5,9):
                            option_description=str(row[i].value).replace('\n','<br>')                               

                            if i-4 == row[9].value :
                                o = Option(description=option_description,value=row[4].value,question=q)
                            else:
                                o = Option(description=option_description,value=-round((row[4].value/3),4),question=q)

                            o.save()

                        if not  test_type == "general":
                            test_object = Test.objects.get(id=test_ID)
                            test_object.question.add(q.id)
                            test_object.save()
                    
                        
                        for cell in row:
                            
                            row_data.append(str(cell.value))
                        excel_data.append(row_data)
                    else:
                        error_rows.append(str(count+1) + " " +  row[0].value )

                except:

                    error_rows.append(str(count+1) + " " +  row[0].value )
                    continue


            series=Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))
            courses= Course.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))
            daily_mcq_tests=Test.objects.filter(daily_mcq__isnull=False,created_by=request.user,open_date__gt=date.today())
            scholarship=Scholarship_Test.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))
            
            
            context =      {
                'series' : series,
                'courses': courses,
                'daily_mcq_tests'   : daily_mcq_tests,
                'scholarship' : scholarship,
                'excel_data' : excel_data,
                'error_rows' :error_rows,

                }

            return render(request, 'quest.html', context)
    else:
        return render(request, 'quest.html', {})


def load_tests(request):
    series_id = request.GET.get('series')
    
    tests = Test.objects.filter(test_series=series_id)
    return render(request, 'question/test_dropdown_list_options.html', {'tests': tests})


def load_course_tests(request):
    course_id = request.GET.get('course')    
    tests = Test.objects.filter(course_part__course=course_id)  
    return render(request, 'question/test_dropdown_list_options.html', {'tests': tests})

def load_daily_mcq_tests(request):
    course_id = request.GET.get('course')    
    tests = Test.objects.filter(course_part__course=course_id)  
    return render(request, 'question/test_dropdown_list_options.html', {'tests': tests})

def load_sholarship_tests(request):
    scholarship_ID = request.GET.get('scholarship_ID')
    tests = Test.objects.filter(scholarship_test=scholarship_ID)  
    return render(request, 'question/test_dropdown_list_options.html', {'tests': tests})


def signup(request):
    if not request.user.is_anonymous:
        return redirect('home')
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES )
        if form.is_valid():
            signup = form.save(commit=False)
            password= random.randint(1000,9999) 
            signup.password=make_password(str(password))
            
            daf=interview_quidance=form.cleaned_data['daf']
            if daf:
                signup.interview_quidance=True

            signup.username=form.cleaned_data['email']
            signup.save()
            group=Group.objects.get(name="Student")
            signup.groups.add(group)

            user = form.save()
            if daf:
                course=Course.objects.get(title="Interview Guidance Programme 2020")
                Course_Enrolment.objects.create(course=course, user=user,joined_on= date.today())

          
            #send mail
            email=form.cleaned_data.get('email')
            website='http://portal.kpriasacademy.in/'
        
            subject = 'KPR IAS Academy Portal'
            message = 'Hi, \nThanks for joining in our Academy, \n1. Click the below website link to login to the portal. \n2. Sign in with given below username & Password. \n3. Complete your profile. Your admission process will get completed, once you submitted your profile. \n \nWebsite: {}  \n\nLogin Crendentials:  \n   Username: {} \n   Password: {}  \n\nThankyou \nKPR IAS ACADEMY'.format(website,email,password)
        
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [email , ] 
            send_mail( subject, message, email_from, recipient_list )
           
            return redirect('registered')
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})
    

    
    
    

def registered(request):
    return render(request,'account/registered.html', {})
    
    
    
@login_required(login_url='login') 
def contact_us(request):  
   
    return render(request, 'contact_us.html', {})


@login_required(login_url='login') 
def course_enrolment_batch_update(request,course_enrolment_id):
    if request.method == 'POST':
        batch=request.POST.get('batch')
        Course_Enrolment.objects.filter(id=course_enrolment_id).update(batch_id=batch)
        return redirect('batch_update')

@login_required(login_url='login') 
def print_pdf(request,pk):  
    user=User.objects.get(id=pk)
    if request.user.is_staff:
        if user.once_submited:
            return render(request,'admin/pdf_print.html', {'user':user,})
        else:
            return HttpResponse(" Profile not completed, kindly check it.")
    else:
        return HttpResponse("Permission Denied..!")


@login_required(login_url='login') 
def batch_update(request):    
    course_enrolments=Course_Enrolment.objects.filter(user=request.user)
    batches=Batch.objects.all()
    return render(request,'account/batch_update.html', {'course_enrolments':course_enrolments,'batches':batches,})


@login_required(login_url='login') 
def view_profile(request):    
    user=User.objects.get(username=request.user)
    return render(request,'account/view_profile.html', {'user':user,})



class EnquiryView(APIView):
    def post(self,request,format=None):
        payload = json.dumps(request.data)
        payload = json.loads(payload)
        try:
            enquiry= Enquiry(name=payload['name'],email=payload['email'],mobile_number=payload['mobile_number'],alternate_mobile_number=payload['alternate_mobile_number'],message=payload['message'])
            enquiry.save()
            return Response("Success", status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'error': 'Something terrible went wrong,contact your adminstrator.'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
              
        
