from django.shortcuts import render
from .models import Mains_Test_Series
from assignment.models import Assignment,Submission,AFile
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from account.models import Mains_Test_Series_Enrolment
from .forms import SubmissionForm
from django.shortcuts import redirect
from django.http import HttpResponse
from assignment.models import Assignment
from account.views import complete_profile


# Create your views here.


@complete_profile
def mains_test_series_list(request):
    series=Mains_Test_Series.objects.filter(start_date__lte=date.today(), end_date__gte=date.today(),active=True).order_by('-start_date')
    return render(request, 'mains_test_series/series_list.html', {'series':series,})

@complete_profile
@login_required(login_url='login')
def mains_test_series_detail(request,series):      
    if Mains_Test_Series_Enrolment.objects.filter(series=series,user=request.user).exists() or request.user.groups.filter(name='Instructor').exists():
        


        if request.method == 'POST':
            submission=Submission.objects.filter(assignment_id=request.POST['assignment_id'] ,user=request.user).delete()

            assignment_id= request.POST['assignment_id']
            s_file = request.FILES['file']
            submission=Submission(assignment_id=assignment_id,user=request.user,status="S",marks="0",sfile=s_file)
            submission.save()        
            assignments=Assignment.objects.filter(test_series=series)
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
        
            return redirect('mains_test_series_detail', series=submission.assignment.test_series.id)
      


                 
        else:
            assignments=Assignment.objects.filter(test_series=series) 
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
        
            return render(request, 'mains_test_series/view_mains_test_series.html', {'assignments':assignments,'day':d1,})


    return HttpResponse("You don't have rights to access the test series")



@complete_profile
@login_required(login_url='login')
def mains_test(request,assignment_id):
    if not Mains_Test_Series_Enrolment.objects.filter(series__assignment=assignment_id,user=request.user).exists():
        return HttpResponse("You don't have rights to access the test series")
    if request.method == 'POST': 

            
        redirect('mains_test_series_detail', series=submission.assignment.test_series.id)
      
    else:        
        if Submission.objects.filter(assignment_id=assignment_id,user=request.user):            
            assignment=None
        else:
            assignment=Assignment.objects.get(id=assignment_id,)
        
        afile=AFile.objects.get(assignment=assignment) 
        form = SubmissionForm()

        return render(request, 'mains_test_series/view_assignment.html', {'assignment':assignment,'afile':afile,'form':form,}) 


@complete_profile
@login_required(login_url='login')
def mains_test_result(request,assignment_id):

    if  Submission.objects.filter(user=request.user,status='A',assignment=assignment_id).exists():
        submission=Submission.objects.get(user=request.user,assignment=assignment_id)
        return render(request, 'mains_test_series/view_result.html', {'submission':submission})

@complete_profile
@login_required(login_url='login')
def mains_performance(request,pk):

    if  Mains_Test_Series_Enrolment.objects.filter(series__id=pk,user=request.user).exists():
        #Attempted Progress in a Module

        test_names = list()
        score = list ()  
        submitted_on = list ()       
        tests = Assignment.objects.filter(test_series=pk).order_by('open_date')
        count=1
        for  test in tests:  

            #Attempted Progress in a Module
            test_names.append(test.title)
            try:
                mark=Submission.objects.get(assignment=test,user=request.user)
                score.append(mark.marks)
                dt=mark.submitted_on
                dt=mark.submitted_on.strftime("%d-%m-%Y")
                submitted_on.append(str(dt))
                
            except:               
                score.append(0)
                submitted_on.append('Not Submitted')


            if count == 1:
                series=Assignment.objects.get(id=test.id)
                series_name=series.test_series

            else:
                pass

            count+=count
           

        context =      {
            'test_names' : test_names,
            'score' : score,
            'series_name':series_name,
            'submitted_on':submitted_on,
      
          }

        return render(request,'mains_test_series/performance.html',context)


    else:
        return HttpResponse('You are not allowed to view this page.')