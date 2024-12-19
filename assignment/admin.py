from django.contrib import admin
from .models import Assignment,Submission,AFile
from account.models import User
from django.contrib.admin import ModelAdmin, SimpleListFilter
from mains_test_series.models import Mains_Test_Series
from django.db.models import Q
from course.models import Course
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from . import models


# Register your models here.

class AFileInline(admin.TabularInline):
    model = AFile
    extra = 0
    

class SubmissionInline(admin.TabularInline):   
    model = Submission
    extra = 0
    fields = ('user','submitted_on','marks','sfile' ,'corrected_answer_sheet','status')
    readonly_fields = ('submitted_on','user' )
    


    

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines=[AFileInline,SubmissionInline]
    exclude=['created_by']
    readonly_fields=('test_series','part')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "moderator":
            kwargs["queryset"] = User.objects.filter(groups__name='Instructor')
        return super(AssignmentAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
            
            

           
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user          
 
        super().save_model(request, obj, form, change)

def assign_90_mark(modeladmin, news, queryset):
    queryset.update(marks=90)
assign_90_mark.marks = u"Put 95 Marks"


class Mains_Test_Series_Filter(SimpleListFilter):  
  title = ('Mains Test Series')
  parameter_name = 'series'
  
  def lookups(self, request, model_admin):
    if request.user.is_superuser:
        qs_series = Mains_Test_Series.objects.filter(active=True)

    elif request.user.groups.filter(name='Instructor').exists():
        qs_series = Mains_Test_Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True) 
        
  

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


class CourseFilter(SimpleListFilter):  
  title = ('Course')
  parameter_name = 'course'
  
  def lookups(self, request, model_admin):
    if request.user.is_superuser:
        qs_course = Course.objects.filter(active=True)

    elif request.user.groups.filter(name='Instructor').exists():
        qs_course = Course.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True) 
        
  

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



class MainsFilter(SimpleListFilter):  
  title = ('Mains')
  parameter_name = 'mains'
  
  def lookups(self, request, model_admin):

    series=request.GET.get('series', None)  
    course=request.GET.get('course', None)   
            
    if request.user.is_superuser:
        if series:
            qs_assignment = Assignment.objects.filter(test_series=series)
        elif course:
           
            qs_assignment = Assignment.objects.filter(part__course=course)
            
        else:
            qs_assignment = Assignment.objects.all()

    elif request.user.groups.filter(name='Instructor').exists():

        if series:
            qs_assignment = Assignment.objects.filter(test_series=series)

        elif course:
            qs_assignment = Assignment.objects.filter(part__course=course)

        else:
            qs_assignment = Assignment.objects.filter(Q(test_series__created_by=request.user) | Q(test_series__moderator=request.user) | Q(part__course__created_by=request.user) | Q(part__course__moderator=request.user)) 
        
 
    list_assignment = []
    for assignment in qs_assignment:
        list_assignment.append(
            (assignment.id, assignment.title)
        )
    return (
        sorted(list_assignment, key=lambda tp:tp[1])
    ) 

  def queryset(self, request, queryset):
      return queryset


 
class SubmissionResource(resources.ModelResource):



  assignment = fields.Field(
    column_name ="Mains Test",
    attribute='assignment',
    widget= ForeignKeyWidget(models.Assignment,'title')
  )

  user__first_name = fields.Field(
    column_name ="First Name",
    attribute='user__first_name',
 
  )
  user__last_name = fields.Field(
    column_name ="Last Name",
    attribute='user__last_name',
 
  )

  user__email = fields.Field(
    column_name ="Email",
    attribute='user__email',
 
  )

  
  

  class Meta:
    model = Submission

    fields = ('user__first_name','user__last_name','assignment','marks','user__email','submitted_on')
    exclude=('id',)
    export_order = ["user__first_name", "user__last_name", "assignment", "marks","user__email","submitted_on"]


@admin.register(Submission)
class SubmissionAdmin(ImportExportModelAdmin):
    resource_class = SubmissionResource
    list_display = ('user','assignment','marks','submitted_on','status') 
    list_filter = (Mains_Test_Series_Filter,CourseFilter,MainsFilter,'status')
    search_fields =['user']



    def get_queryset(self, request): 
          series=request.GET.get('series', None)  
          course=request.GET.get('course', None) 
          mains=request.GET.get('mains', None)   
               
         
          if request.user.is_superuser:
              if series:
                  if mains:
                      return Submission.objects.filter(assignment__test_series=series,assignment=mains)

                  else:
                      return Submission.objects.filter(assignment__test_series=series) 
              elif course:
                  if mains:
                      return Submission.objects.filter(assignment__part__course=course,assignment=mains)
                  else:
                      return Submission.objects.filter(assignment__part__course=course)    

                 
                  

              else:
                  return Submission.objects.filter(assignment__test_series__active=True,)

          elif request.user.groups.filter(name='Instructor').exists():
              if series:
                  if mains:
                      return Submission.objects.filter(Q(assignment__test_series__created_by=request.user) | Q(assignment__test_series__moderator=request.user) | Q(assignment__part__course__created_by=request.user) | Q(assignment__part__course__moderator=request.user),assignment__test_series=series,assignment=mains)
                  else:
                      return Submission.objects.filter(Q(assignment__test_series__created_by=request.user) | Q(assignment__test_series__moderator=request.user) | Q(assignment__part__course__created_by=request.user) | Q(assignment__part__course__moderator=request.user),assignment__test_series=series)    

  
              elif course:
                  if mains:
                      return Submission.objects.filter(assignment__part__course=course,assignment=mains)
                  else:
                      return Submission.objects.filter(assignment__part__course=course)    
                 

              else:
                  return Submission.objects.filter(Q(assignment__test_series__created_by=request.user) | Q(assignment__test_series__moderator=request.user) | Q(assignment__part__course__created_by=request.user) | Q(assignment__part__course__moderator=request.user))