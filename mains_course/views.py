from django.shortcuts import render
from .models import Course_Test_Series
from assignment.models import Assignment,Submission,AFile,SFile
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from account.models import Mains_Course_Test_Series_Enrolment
from .forms import SubmissionForm,SForm
from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.



def mains_course_list(request):
    series=Course_Test_Series.objects.filter(start_date__lte=datetime.today(), end_date__gte=date.today(),active=True).order_by('-start_date')
    return render(request, 'mains_course/series_list.html', {'series':series,})


@login_required(login_url='login')
def mains_course_detail(request,series):      
    if Mains_Course_Test_Series_Enrolment.objects.filter(series=series,user=request.user).exists() or request.user.groups.filter(name='Instructor').exists():
        assignments=Assignment.objects.filter(course=series) 
        
        return render(request, 'mains_course/view_mains_test_series.html', {'assignments':assignments,})

    return HttpResponse("You don't have rights to access the test series")




@login_required(login_url='login')
def course_mains_test(request,assignment_id):
    if not Mains_Course_Test_Series_Enrolment.objects.filter(series__assignment=assignment_id,user=request.user).exists():
        return HttpResponse("You don't have rights to access the test series")
    if request.method == 'POST':    
        form = SubmissionForm(request.POST)
        sfileform = SForm(request.POST, request.FILES)
        submission=Submission.objects.filter(assignment_id=assignment_id,user=request.user)
        if not submission:
            if form.is_valid() and sfileform.is_valid():
                submission = form.save(commit=False)
                submission.assignment_id=assignment_id
                submission.user=request.user
                submission.marks=0
                submission.status='S'
                submission = form.save()
                sfile = sfileform.save(commit=False)
                sfile.submission=submission
                sfile=sfileform.save()


            
            return redirect('mains_course_detail', series=submission.assignment.course.id)
        else:
            return redirect('/')

 
    else:        
        if Submission.objects.filter(assignment_id=assignment_id,user=request.user):            
            assignment=None
        else:
            assignment=Assignment.objects.get(id=assignment_id,)
        
        afile=AFile.objects.filter(assignment=assignment) 
        form = SubmissionForm()
        sfileform = SForm()
        return render(request, 'mains_course/view_assignment.html', {'assignment':assignment,'afiles':afile,'form':form,'sfileform':sfileform,}) 



@login_required(login_url='login')
def course_mains_test_result(request,assignment_id):

    if  Submission.objects.filter(user=request.user,status='A',assignment=assignment_id).exists():
        submission=Submission.objects.get(user=request.user,assignment=assignment_id)
        return render(request, 'mains_course/view_result.html', {'submission':submission}) 
