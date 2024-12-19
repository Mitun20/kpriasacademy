# Register your models here.
from django.contrib import admin
from .models import Test,Question,Option,Attempt,Response,On_Test
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
import math
from account.models import User
from django.db.models import Sum
from django import forms
from django.db.models import Q
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from subject.models import Subject
from django.contrib.admin.filters import RelatedOnlyFieldListFilter
from django.contrib.admin import ModelAdmin, SimpleListFilter
from tseries.models import Series
from course.models import Course
from . import models

from scholarship.models import Scholarship_Test


# Register your models here.

class TestForm(forms.ModelForm):
    
    class Meta:
        model = Test
        fields=['name','description','instruction','open_date','close_date','test_series','total_no_questions','total_marks','duration_in_minutes','question','show_answers','live_discussion_link','live_discussion_date','active']

    def clean(self):
        if self.cleaned_data.get('active'):
            total_mark = self.cleaned_data.get('total_marks') 
           
            get_mark=Question.objects.filter(id__in=self.cleaned_data.get('question')).aggregate(Sum('mark'))['mark__sum']
            if total_mark == get_mark:
                return self.cleaned_data
            else:
                raise forms.ValidationError("Given Total marks and question sum marks not matched")    
            
              

            if len(self.cleaned_data.get('question')) !=  self.cleaned_data.get('total_no_questions'):
                
                 raise forms.ValidationError("Given total no of question and choosed question count not matched")    
            



@admin.register(On_Test)
class On_TestAdmin(admin.ModelAdmin):
    list_display=['user',]
    list_filter=['started_time','test']
    


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('question',)
    form = TestForm
    search_fields=['name']
    list_filter=['test_series','daily_mcq','course_part','scholarship_test']
    readonly_fields = ('daily_mcq','test_series','scholarship_test','course_part')
    fields=['name','description','instruction','open_date','close_date','test_series','daily_mcq','scholarship_test','course_part','total_no_questions','total_marks','duration_in_minutes','question','subject','discussion_video_link','active','show_answers','live_discussion_link','live_discussion_date','negative_mark']
    change_form_template = "admin/question_upload.html"
    change_list_template = 'question_admin.html'


    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "moderator":
            kwargs["queryset"] = User.objects.filter(groups__name='Instructor')
        return super(TestAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
            
            

           
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user          
 
        super().save_model(request, obj, form, change)


    def get_queryset(self, request):           
         
          if request.user.is_superuser: 
              return super(TestAdmin, self).get_queryset(request)

          elif request.user.groups.filter(name='Instructor').exists():
              return Test.objects.filter(Q(test_series__created_by=request.user) | Q(test_series__moderator=request.user) | Q(course_part__course__created_by=request.user) | Q(course_part__course__moderator=request.user) | Q(scholarship_test__created_by=request.user) | Q(scholarship_test__moderator=request.user) | Q(daily_mcq__created_by=request.user) | Q(created_by=request.user))
          elif request.user.groups.filter(name='Super_staff').exists():
              return Test.objects.filter(Q(test_series__created_by=request.user) | Q(test_series__moderator=request.user) | Q(course_part__course__created_by=request.user) | Q(course_part__course__moderator=request.user) | Q(scholarship_test__created_by=request.user) | Q(scholarship_test__moderator=request.user) | Q(daily_mcq__created_by=request.user) | Q(created_by=request.user))
           
          



class OptionFormSet(BaseInlineFormSet):
    '''
    Validate formset data here
    '''
    def clean(self):
        super(OptionFormSet, self).clean()
        
        assigned_mark=self.instance.mark
        correct_answer_count = 0
        non_zero_count = 0
        for form in self.forms:           
          
            if not hasattr(form, 'cleaned_data'):
                continue

            data = form.cleaned_data

            if not data.get('description'):
                continue
                        
            if data.get('value') == assigned_mark:
                correct_answer_count+=1 

           
            if data.get('value') > float(0.0):
                non_zero_count+=1 
           
            if form.cleaned_data['value'] <= 0.0: 
                form.instance.value = -round((assigned_mark/3),3)
                
            
        if correct_answer_count != 1 or non_zero_count > 1:
            raise ValidationError('Question should have exaclty only one Correct Option ')


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4
    formset = OptionFormSet
    

class QuestionResource(resources.ModelResource):


  subject = fields.Field(
    column_name ="subject_name",
    attribute='subject',
    widget= ForeignKeyWidget(Subject,'name')
  )

  class Meta:
    model = Question

class OptionResource(resources.ModelResource):


  subject = fields.Field(
    column_name ="name",
    attribute='question',
    widget= ForeignKeyWidget(Question,'name')
  )

  class Meta:
    model = Option


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = ('name',)
    inlines=[OptionInline]
    list_filter=['subject']
    search_fields=['name']
    change_list_template = 'question_admin.html'
    

@admin.register(Option)
class OptionAdmin(ImportExportModelAdmin):
    resource_class = OptionResource
    list_display=['description','value','question']



class DailyMcqFilter(SimpleListFilter):  
  title = ('Daily Mcq')
  parameter_name = 'daily_mcq'
  
  def lookups(self, request, model_admin):
    grade=request.GET.get('grade', None)
    if request.user.is_superuser:
        qs_test = Test.objects.filter(daily_mcq__isnull=False)

    elif request.user.groups.filter(name='Instructor').exists():
        qs_test = Test.objects.filter(created_by=request.user,daily_mcq__isnull=False) 
        
    elif request.user.groups.filter(name='Super_Staff').exists():
        qs_test = Test.objects.filter(created_by=request.user,daily_mcq__isnull=False)


    list_test = []
    for test in qs_test:
        list_test.append(
            (test.id, test.name)
        )
    return (
        sorted(list_test, key=lambda tp:tp[1])
    ) 

  def queryset(self, request, queryset):
      return queryset


class PrelimsFilter(SimpleListFilter):  
  title = ('Prelims Test Series')
  parameter_name = 'prelims'
  
  def lookups(self, request, model_admin):
    grade=request.GET.get('grade', None)
    if request.user.is_superuser:
        qs_series = Series.objects.all()
        

    elif request.user.groups.filter(name='Instructor').exists():
        qs_series = Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))
        


    list_series = []
    for series in qs_series:
        list_series.append(
            (series.id, series.title)
        )
    return (
        sorted(list_series, key=lambda tp:tp[1])
    ) 

  def queryset(self, request, queryset):
      return queryset



class TestFilter(SimpleListFilter):  
  title = ('Test')
  parameter_name = 'test'
  
  def lookups(self, request, model_admin):
    prelims=request.GET.get('prelims', None)

    scholarship_test=request.GET.get('scholarship_test', None)
    course_part_test=request.GET.get('course_part_test', None)


    qs_test=[]
    if request.user.is_superuser:
        if prelims:
            qs_test =Test.objects.filter(test_series=prelims)

        elif scholarship_test:            
            qs_test =Test.objects.filter(scholarship_test=scholarship_test)

        elif course_part_test:            
            qs_test =Test.objects.filter(course_part__course=course_part_test)



        

    elif request.user.groups.filter(name='Instructor').exists():
       if prelims:
            qs_test =Test.objects.filter(test_series=prelims)

       elif scholarship_test:
            qs_test =Test.objects.filter(scholarship_test=scholarship_test)


       elif course_part_test:
            qs_test =Test.objects.filter(course_part=course_part_test)





    elif request.user.groups.filter(name='Staff User').exists():

       if scholarship_test:
            qs_test =Test.objects.filter(scholarship_test=scholarship_test)


       elif course_part_test:
            qs_test =Test.objects.filter(course_part=course_part_test)


        

    list_test = []
    for test in qs_test:
        list_test.append(
            (test.id, test.name)
        )
    return (
        sorted(list_test, key=lambda tp:tp[1])
    ) 

  def queryset(self, request, queryset):
      return queryset


class ScholarshipFilter(SimpleListFilter):  
  title = ('Scholarship Test')
  parameter_name = 'scholarship_test'
  
  def lookups(self, request, model_admin):
    qs_scholarship=[]
    if request.user.is_superuser:
        qs_scholarship =Scholarship_Test.objects.all()
         

    elif request.user.groups.filter(name='Super_Staff').exists():
        qs_scholarship =Scholarship_Test.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))

        

    list_scholarship = []
    for scholarship in qs_scholarship:
        list_scholarship.append(
            (scholarship.id, scholarship.title)
        )
    return (
        sorted(list_scholarship, key=lambda tp:tp[1])
    ) 

  def queryset(self, request, queryset):
      return queryset



class CoursePartFilter(SimpleListFilter):  
  title = ('Course Part')
  parameter_name = 'course_part_test'
  
  def lookups(self, request, model_admin):
    grade=request.GET.get('grade', None)
    if request.user.is_superuser:
        qs_course = Course.objects.all()
        

    elif request.user.groups.filter(name='Instructor').exists():
        qs_course = Course.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))
        
 

    list_course = []
    for course in qs_course:
        list_course.append(
            (course.id, course.title)
        )
    return (
        sorted(list_course, key=lambda tp:tp[1])
    ) 

  def queryset(self, request, queryset):
      return queryset


class Attemptesource(resources.ModelResource):

  user__first_name = fields.Field(
    column_name ="First Name",
    attribute='user__first_name',
   
  )

  user__last_name = fields.Field(
    column_name ="Last Name",
    attribute='user__last_name',
   
  )


  user__email = fields.Field(
    column_name ="Registered Email",
    attribute='user__email',
   
  )


  test = fields.Field(
    column_name ="Test",
    attribute='test',
    widget= ForeignKeyWidget(models.Test,'name')
  )


  rank = fields.Field(
    column_name ="rank",
    attribute='rank',
 
  )


  attempted_questions = fields.Field(
    column_name ="Attempted Questions",
    attribute='attempted_questions',
 
  )

  correct = fields.Field(
    column_name ="Correct",
    attribute='correct',
 
  )

  incorrect = fields.Field(
    column_name ="Incorrect",
    attribute='incorrect',
 
  )

  user__admission_number = fields.Field(
    column_name ="Admission Number",
    attribute='user__admission_number'
   )

  user__mobile_number = fields.Field(
    column_name ="Mobile Number",
    attribute='user__mobile_no'
   )



  class Meta:
    model = Attempt
    fields = ('user__admission_number','user__first_name','user__last_name','user__email','user__mobile_number','attempted_questions','correct','incorrect','test','score','rank')
    exclude=('id','series')
    export_order=('user__admission_number','test','user__first_name','user__last_name','user__email','user__mobile_number','attempted_questions','correct','incorrect','score','rank')


@admin.register(Attempt)
class AttemptAdmin(ImportExportModelAdmin):
    list_display = ('first_name','last_name','attempted_questions','correct','incorrect','test','score','rank')
    date_hierarchy = 'start_date_time'
    search_fields=['user','test']
    resource_class = Attemptesource
    list_filter=[DailyMcqFilter,PrelimsFilter,ScholarshipFilter,CoursePartFilter,TestFilter]


    def get_queryset(self, request):
        daily_mcq_test_id=request.GET.get('daily_mcq', None) 
        prelims_id=request.GET.get('prelims', None) 
        test_id=request.GET.get('test', None)
        scholarship_test_id=  request.GET.get('scholarship_test', None)   
        course_part_test= request.GET.get('course_part_test', None)   
         
        if request.user.is_superuser:
            if daily_mcq_test_id:
                return Attempt.objects.filter(test=daily_mcq_test_id)
            elif prelims_id:
                if test_id:                    
                    return Attempt.objects.filter(test__test_series=prelims_id,test=test_id)

               
                return Attempt.objects.filter(test__test_series=prelims_id)

            elif scholarship_test_id:
                if  test_id:
                    return Attempt.objects.filter(test__scholarship_test=scholarship_test_id,test=test_id)
                return Attempt.objects.filter(test__scholarship_test=scholarship_test_id)
            
            elif course_part_test:
                return Attempt.objects.filter(test__course_part__course=course_part_test)
        

            else:
                return Attempt.objects.all()



        elif request.user.groups.filter(name='Instructor').exists():              
            if daily_mcq_test_id:
                return Attempt.objects.filter(test=daily_mcq_test_id)

            elif prelims_id:
                if test_id:
                    return Attempt.objects.filter(test__test_series=prelims_id,test=test_id)
               
                return Attempt.objects.filter(test__test_series=prelims_id)

            elif scholarship_test_id:
                if  test_id:
                    return Attempt.objects.filter(test__scholarship_test=scholarship_test_id,test=test_id)
                return Attempt.objects.filter(test__scholarship_test=scholarship_test_id)
            
            elif course_part_test:
                return Attempt.objects.filter(test__course_part__course=course_part_test)
        


            else:
                return Attempt.objects.filter(Q(test__test_series__created_by=request.user) | Q(test__test_series__moderator=request.user)  | Q(test__course_part__course__created_by=request.user) | Q(test__course_part__course__moderator=request.user) | Q(test__scholarship_test__created_by=request.user) | Q(test__scholarship_test__moderator=request.user) | Q(test__created_by=request.user))


        elif request.user.groups.filter(name='Super_Staff').exists():              
            if daily_mcq_test_id:
                return Attempt.objects.filter(test=daily_mcq_test_id)

            elif scholarship_test_id:
                if  test_id:
                    return Attempt.objects.filter(test__scholarship_test=scholarship_test_id,test=test_id)

                return Attempt.objects.filter(test__scholarship_test=scholarship_test_id)


            else:
                return Attempt.objects.filter(Q(test__test_series__created_by=request.user) | Q(test__test_series__moderator=request.user)  | Q(test__course_part__course__created_by=request.user) | Q(test__course_part__course__moderator=request.user) | Q(test__scholarship_test__created_by=request.user) | Q(test__scholarship_test__moderator=request.user),test__created_by=request.user)
    

    



@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user','attempt','option','question')
