from django.contrib import admin
from . import models
from .models import User,Test_Series_Enrolment,Course_Enrolment,Scholarship_Test_Enrolment,Mains_Test_Series_Enrolment,Educational_Qualification, Family_Details, STD, Relation, Miscellaneous_Fee , Enquiry
from django.contrib.auth.hashers import make_password
from django.contrib import admin
from course.models import Course
from django.db.models import Q
from scholarship.models import Scholarship_Test
from django import forms    
from django.core.exceptions import ValidationError
from tseries.models import Series
from mains_test_series.models import Mains_Test_Series
from django.core.mail import send_mail
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from django.conf import settings 
import random
from django import forms
from django.contrib.admin import  SimpleListFilter


# Register your models here.

admin.site.site_header = "KPR IAS ACADEMY"
admin.site.site_title = "KPR IAS ACADEMY"

class Course_Filter(SimpleListFilter):  
  title = ('Course')
  parameter_name = 'course'

  def lookups(self, request, model_admin):    

    if request.user.is_superuser:
      qs_courses= Course.objects.filter(active=True)
    elif request.user.groups.filter(name='Instructor').exists():
      qs_courses=Course.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)


    list_course = []
    for course in qs_courses:
        list_course.append(
            (course.id, course.title)
        )
    return (
        sorted(list_course, key=lambda tp:tp[1])
    ) 

  def queryset(self, request, queryset):
      return queryset




class Prelims_Filter(SimpleListFilter):  
  title = ('Prelims Test Series')
  parameter_name = 'prelims'

  def lookups(self, request, model_admin):    

    if request.user.is_superuser:
      qs_prelims= Series.objects.filter(active=True)
    elif request.user.groups.filter(name='Instructor').exists():
      qs_prelims=Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)


    list_prelims = []
    for prelims in qs_prelims:
        list_prelims.append(
            (prelims.id, prelims.title)
        )
    return (
        sorted(list_prelims, key=lambda tp:tp[1])
    ) 

  def queryset(self, request, queryset):
      return queryset


class Mains_Filter(SimpleListFilter):  
  title = ('Mains Test Series')
  parameter_name = 'mains'

  def lookups(self, request, model_admin):    

    if request.user.is_superuser:
      qs_mains= Mains_Test_Series.objects.filter(active=True)
    elif request.user.groups.filter(name='Instructor').exists():
      qs_mains=Mains_Test_Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)


    list_mains = []
    for mains in qs_mains:
        list_mains.append(
            (mains.id, mains.title)
        )
    return (
        sorted(list_mains, key=lambda tp:tp[1])
    ) 

  def queryset(self, request, queryset):
      return queryset


class Test_Series_EnrolmentInline(admin.TabularInline):
    model = Test_Series_Enrolment
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "series":

            if request.user.is_superuser:
                kwargs["queryset"] = Series.objects.filter(active=True)
            elif request.user.groups.filter(name='Instructor').exists():
                kwargs["queryset"] = Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)
                      
            return super().formfield_for_foreignkey(db_field, request, **kwargs)




class Course_EnrolmentInline(admin.TabularInline):
    model = Course_Enrolment
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":

            if request.user.is_superuser:
                kwargs["queryset"] = Course.objects.filter(active=True)
            elif request.user.groups.filter(name='Instructor').exists():
                kwargs["queryset"] = Course.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)
                          
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class Scholarship_EnrolmentInline(admin.TabularInline):
    model = Scholarship_Test_Enrolment
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "scholarship_test":
            if request.user.is_superuser:
                kwargs["queryset"] = Scholarship_Test.objects.filter(active=True)
            elif request.user.groups.filter(name='Instructor').exists():
                kwargs["queryset"] = Scholarship_Test.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)
            elif request.user.groups.filter(name='Super_Staff').exists():
                kwargs["queryset"] = Scholarship_Test.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)
            
                     
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

class Mains_Test_Series_EnrolmentInline(admin.TabularInline):
    model = Mains_Test_Series_Enrolment
    extra = 0
    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "series":        
            if request.user.is_superuser:
                kwargs["queryset"] =  Mains_Test_Series.objects.filter(active=True)
            elif request.user.groups.filter(name='Instructor').exists():
                kwargs["queryset"] = Mains_Test_Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)
            
                   
                        
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields=('email','groups','admission_number','first_name','first_name','gender','college_work','age','mobile_no','native','parents_mobile_no','batch','date','regular','weekend','hostel','study_hall','merit','received_amount','hostel_fees','hostel_fees_paid_date','profile_picture','signature_of_the_applicant','once_submited','under','password')

    def clean(self):
      pass
  
class UserResource(resources.ModelResource):

  date_joined = fields.Field(
    column_name ="DOJ",
    attribute='date_joined'
   )


  degree = fields.Field(
    column_name ="Degree",
    attribute='degree'
   )


  gender = fields.Field(
    column_name ="Gender",
    attribute='get_gender_display'
   )

  under = fields.Field(
    column_name ="Under",
    attribute='gunder'
   )


  age = fields.Field(
    column_name ="Age",
    attribute='age'
   )

  college_work = fields.Field(
    column_name ="College/Work",
    attribute='college_work'
   )



  mobile_no = fields.Field(
    column_name ="Ph",
    attribute='mobile_no'
   )


  native = fields.Field(
    column_name ="Native",
    attribute='native'
   )



  
  under = fields.Field(
    column_name ="Under",
    attribute='under'
   )

  get_full_name = fields.Field(
    column_name ="Name",
    attribute='get_full_name'
   )



  admission_number = fields.Field(
    column_name ="Admission Number",
    attribute='admission_number',
   
  )


  parents_mobile_no = fields.Field(
    column_name ="Parents no",
    attribute='parents_mobile_no',
   
  )

  batch = fields.Field(
    column_name ="Batch",
    attribute='batch',
   
  )

  organization_fees = fields.Field(
    column_name ="Org fee",
    attribute='organization_fees',
   
  )


  scholarship = fields.Field(
    column_name ="Scholar",
    attribute='scholarship',
   
  )

  academic_fees = fields.Field(
    column_name ="Academic",
    attribute='academic_fees',
   
  )


  hostel_fees = fields.Field(
    column_name ="Hostel",
    attribute='hostel_fees',
   
  )


  ttl = fields.Field(
    column_name ="TTL",
    attribute='ttl',
   
  )


  admission_fees = fields.Field(
    column_name ="admiss fee",
    attribute='miscellaneous_fee',
   
  )

  gst = fields.Field(
    column_name ="GST",
    attribute='gst',
   
  )


  mode_of_payment = fields.Field(
    column_name ="Mode of payment",
    attribute='mode_of_payment',
   
  )

  email = fields.Field(
    column_name ="Mail id",
    attribute='email',
   
  )


  


  course_facility = fields.Field(
    column_name ="Course/Facility",
    attribute='course_facility',
   
  )


  class Meta:
    model = User
    fields = ('admission_number','date_joined','get_full_name','gender','under','degree','college_work','age','mobile_no','native','parents_mobile_no','batch','organization_fees','scholarship','academic_fees','hostel_fees','ttl','course_facility','admission_fees','gst','mode_of_payment','email')
    exclude=('id',)
    export_order = ('admission_number','date_joined','get_full_name','gender','under','degree','college_work','age','mobile_no','native','parents_mobile_no','batch','organization_fees','scholarship','academic_fees','hostel_fees','ttl','course_facility','admission_fees','gst','mode_of_payment','email')


class Educational_Qualification_Inline(admin.TabularInline):
    model = Educational_Qualification
    extra = 0


class Family_Details_Inline(admin.TabularInline):
    model = Family_Details
    extra = 0


class Miscellaneous_Fee_Inline(admin.TabularInline):
    model = Miscellaneous_Fee
    extra = 0
    readonly_fields = ('paid_date',)


@admin.register(User)
class UserModelAdmin(ImportExportModelAdmin):
    form =UserForm
    resource_class = UserResource
    search_fields=['email',]
    list_display = ('get_full_name','mobile_no','username')
    list_filter=['date_joined',Course_Filter,Prelims_Filter,Mains_Filter,'groups','current_status_upsc',]
    inlines=[Educational_Qualification_Inline,Family_Details_Inline,Test_Series_EnrolmentInline,Mains_Test_Series_EnrolmentInline,Course_EnrolmentInline,Scholarship_EnrolmentInline,Miscellaneous_Fee_Inline]
    change_form_template = 'admin/user_change_form.html'


    def get_queryset(self, request):
        #getting values from url parameter
        course=request.GET.get('course', None)
        prelims=request.GET.get('prelims', None)
        mains=request.GET.get('mains', None)

        if course:
          if prelims:
            if mains:
              get_users=Course_Enrolment.objects.filter(user__course_enrolment__course=course,user__test_series_enrolment__series=prelims,user__mains_test_series_enrolment__series=mains,).values_list('user__id', flat=True)
            else:
              get_users=Course_Enrolment.objects.filter(user__course_enrolment__course=course,user__test_series_enrolment__series=prelims).values_list('user__id', flat=True)
          else:
            if mains:
              get_users=Course_Enrolment.objects.filter(course=course,user__mains_test_series_enrolment__series=mains).values_list('user__id', flat=True)
            else:
              get_users=Course_Enrolment.objects.filter(course=course).values_list('user__id', flat=True)
          return User.objects.filter(id__in=get_users)

        elif prelims:
          if mains:
            get_users=Test_Series_Enrolment.objects.filter(series=prelims,user__mains_test_series_enrolment__series=mains).values_list('user__id', flat=True)
          else:
            get_users=Test_Series_Enrolment.objects.filter(series=prelims).values_list('user__id', flat=True)
          return User.objects.filter(id__in=get_users)
        elif mains:
          get_users=Mains_Test_Series_Enrolment.objects.filter(series=mains).values_list('user__id', flat=True)
          return User.objects.filter(id__in=get_users)
        else:
          return super(UserModelAdmin, self).get_queryset(request)

    def save_model(self, request, obj, form, change):
        if not change:  

            password= random.randint(1000,9999)                    
            obj.password = make_password(str(password))
          
            #send mail
            email=form.cleaned_data.get('email')
            website='http://portal.kpriasacademy.in/'
        
            subject = 'KPR IAS Academy Portal'
            message = 'Login Crendentials: \n username: {} \n and password: {} \n website: {}'.format(email,password,website)
        
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [email , ] 
            #send_mail( subject, message, email_from, recipient_list )
            

        if 'password' in form.changed_data:
            obj.password = make_password(form.cleaned_data.get('password')) 

   
                    
        obj.username= form.cleaned_data.get('email')
        super().save_model(request, obj, form, change)


@admin.register(STD)
class STDModelAdmin(admin.ModelAdmin):
    list_display = ('name',)



@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ('name',)


'''   
class PrelimsResource(resources.ModelResource):

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


  series = fields.Field(
    column_name ="Prelims Test Series",
    attribute='series',
    widget= ForeignKeyWidget(models.Series,'title')
  )


  user__address = fields.Field(
    column_name ="Address",
    attribute='user__address',
   
  )

  user__mobile_no = fields.Field(
    column_name ="Mobile Number",
    attribute='user__mobile_no',
   
  )


  
  user__father_name = fields.Field(
    column_name ="Father Name",
    attribute='user__father_name',
   
  )

  joined_on = fields.Field(
    column_name ="Prelims Test Series Registered on",
    attribute='joined_on',
   
  )

  user__admission_number = fields.Field(
    column_name ="Admission Number",
    attribute='user__admission_number'
   )




  class Meta:
    model = Test_Series_Enrolment
    fields = ('user__admission_number','user__first_name','user__last_name','user__email','series','joined_on','user__address','user__mobile_no','user__father_name')
    exclude=('id','series')
    export_order=  ('user__admission_number','user__first_name','user__last_name','user__email','series','joined_on','user__address','user__mobile_no','user__father_name')



@admin.register(Test_Series_Enrolment)
class Test_Series_EnrolmentModelAdmin(ImportExportModelAdmin):
    list_display = ('series','user','admission_number')
    resource_class = PrelimsResource
    list_filter=['joined_on','series',]
    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):  
        if db_field.name == "series":
            if request.user.is_superuser:
                kwargs["queryset"] = Series.objects.filter(active=True)
            elif request.user.groups.filter(name='Instructor').exists():
                kwargs["queryset"] = Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)
            
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def get_queryset(self, request):           
         
          if request.user.is_superuser:
              return super(Test_Series_EnrolmentModelAdmin, self).get_queryset(request)

          elif request.user.groups.filter(name='Instructor').exists():
              
              return Test_Series_Enrolment.objects.filter(Q(series__created_by=request.user) | Q(series__moderator=request.user))

 '''          
   
class CourseResource(resources.ModelResource):

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


  part = fields.Field(
    column_name ="Course",
    attribute='course',
    widget= ForeignKeyWidget(models.Course,'title')
  )


  user__address = fields.Field(
    column_name ="Address",
    attribute='user__address',
   
  )

  user__mobile_no = fields.Field(
    column_name ="Mobile Number",
    attribute='user__mobile_no',
   
  )


  
  user__father_name = fields.Field(
    column_name ="Father Name",
    attribute='user__father_name',
   
  )


  joined_on = fields.Field(
    column_name ="Course Registered on",
    attribute='joined_on',
   
  )

  user__admission_number = fields.Field(
    column_name ="Admission Number",
    attribute='user__admission_number'
   )




  class Meta:
    model = Course_Enrolment
    fields = ('user__admission_number','user__first_name','user__last_name','user__email','part','joined_on','user__address','user__mobile_no','user__father_name')
    exclude=('id','series')
    export_order = ('user__admission_number','user__first_name','user__last_name','part','user__email','joined_on','user__address','user__mobile_no','user__father_name')


class CourseFilter(SimpleListFilter):  
  title = ('Course')
  parameter_name = 'course'

  def lookups(self, request, model_admin):

    if request.user.groups.filter(name__in=['Instructor']).exists():
        qs_course = Course.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)
    else:
        qs_course = Course.objects.filter(active=True)    

  
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

@admin.register(Course_Enrolment)
class Course_EnrolmentModelAdmin(ImportExportModelAdmin):
    list_display = ('admission_number','course','phone_no','user','is_lateral')
    resource_class = CourseResource
    list_filter=[CourseFilter,'batch','joined_on']
    date_hierarchy = 'joined_on'


    def formfield_for_foreignkey(self, db_field, request, **kwargs):  
        if db_field.name == "course":
            if request.user.is_superuser:
                kwargs["queryset"] = Course.objects.filter(active=True)
            elif request.user.groups.filter(name='Instructor').exists():
                kwargs["queryset"] = Course.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)
            
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def get_queryset(self, request):
          course=request.GET.get('course', None)           
         
          if request.user.is_superuser:
              if course:
                return Course_Enrolment.objects.filter(course_id=course)
              else:
                return Course_Enrolment.objects.all()
           
          elif request.user.groups.filter(name='Instructor').exists():
              if course:
                return Course_Enrolment.objects.filter(Q(course__created_by=request.user) | Q(course__moderator=request.user),course_id=course)
              else:
                return Course_Enrolment.objects.filter(Q(course__created_by=request.user) | Q(course__moderator=request.user))
           
  
class ScholarshipResource(resources.ModelResource):

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


  scholarship_test = fields.Field(
    column_name ="Scholarship Test",
    attribute='scholarship_test',
    widget= ForeignKeyWidget(models.Scholarship_Test,'title')
  )


  user__address = fields.Field(
    column_name ="Address",
    attribute='user__address',
   
  )

  user__mobile_no = fields.Field(
    column_name ="Mobile Number",
    attribute='user__mobile_no',
   
  )


  
  user__father_name = fields.Field(
    column_name ="Father Name",
    attribute='user__father_name',
   
  )


  joined_on = fields.Field(
    column_name ="Scholarship Registered on",
    attribute='joined_on',
   
  )

  user__admission_number = fields.Field(
    column_name ="Admission Number",
    attribute='user__admission_number'
   )





  class Meta:
    model = Scholarship_Test_Enrolment

    fields = ('user__admission_number','user__first_name','user__last_name','user__email','scholarship_test','joined_on','user__address','user__mobile_no','user__father_name')
    exclude=('id','series')
    export_order= ('user__admission_number','user__first_name','user__last_name','scholarship_test','user__email','joined_on','user__address','user__mobile_no','user__father_name')


@admin.register(Scholarship_Test_Enrolment)
class Scholarship_Test_EnrolmentModelAdmin(ImportExportModelAdmin):
    list_display = ('scholarship_test','user','admission_number')
    resource_class = ScholarshipResource
    list_filter=['scholarship_test','joined_on']


    def formfield_for_foreignkey(self, db_field, request, **kwargs):  
        if db_field.name == "scholarship_test":
            if request.user.is_superuser:
                kwargs["queryset"] = Scholarship_Test.objects.filter(active=True)
            elif request.user.groups.filter(name='Instructor').exists():
                kwargs["queryset"] = Scholarship_Test.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)
            elif request.user.groups.filter(name='Super_Staff').exists():
                kwargs["queryset"] = Scholarship_Test.objects.filter(Q(created_by=request.user) | Q(moderator=request.user),active=True)
            
            
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def get_queryset(self, request):           
         
          if request.user.is_superuser:
              return super(Scholarship_Test_EnrolmentModelAdmin, self).get_queryset(request)

          elif request.user.groups.filter(name='Super_Staff').exists():
              
              return Scholarship_Test_Enrolment.objects.filter(Q(scholarship_test__created_by=request.user) | Q(scholarship_test__moderator=request.user))


'''
class MainsResource(resources.ModelResource):

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


  series = fields.Field(
    column_name ="Enrolled Mains Test Series",
    attribute='series',
    widget= ForeignKeyWidget(models.Mains_Test_Series,'title')
  )



  user__address = fields.Field(
    column_name ="Address",
    attribute='user__address',
   
  )

  user__mobile_no = fields.Field(
    column_name ="Mobile Number",
    attribute='user__mobile_no',
   
  )


  
  user__father_name = fields.Field(
    column_name ="Father Name",
    attribute='user__father_name',
   
  )

  joined_on = fields.Field(
    column_name ="Mains Registered on",
    attribute='joined_on',
   
  )

  user__admission_number = fields.Field(
    column_name ="Admission Number",
    attribute='user__admission_number'
   )





  class Meta:
    model = Mains_Test_Series_Enrolment
    fields = ('user__admission_number','user__first_name','user__last_name','user__email','series','joined_on','user__address','user__mobile_no','user__father_name')
    exclude=('id','series')
    export_order= ('user__admission_number','user__first_name','user__last_name','series','user__email','joined_on','user__address','user__mobile_no','user__father_name')



@admin.register(Mains_Test_Series_Enrolment)
class Mains_Test_Series_EnrolmentModelAdmin(ImportExportModelAdmin):
    list_display = ('series','user','admission_number')
    resource_class = MainsResource
    list_filter=['series','joined_on']
'''

@admin.register(Enquiry)
class Enquiry_ModelAdmin(ImportExportModelAdmin):
    list_display = ['name','email','mobile_number']
    search_fields = ['name','email','mobile_number']


