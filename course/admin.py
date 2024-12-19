from django.contrib import admin
from .models import Course,Part,Topic,Live_Sessions,Video,Material, Batch
from mcq_test.models import Test
from account.models import User
from django.db.models import Q
from assignment.models import Assignment

from django.contrib.admin.filters import RelatedOnlyFieldListFilter
from tseries.models import Series
from mains_test_series.models import Mains_Test_Series
from . import models

# Register your models here.
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    fields=['name']

class PartInline(admin.TabularInline):
    model = Part
    extra = 0
    fields = ('title', 'part_changeform_link',)
    readonly_fields = ('part_changeform_link', )
    list_filter=['course',]
    can_delete = False


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0
    fields = ('title', 'changeform_link',)
    readonly_fields = ('changeform_link', )
    can_delete = False


   
    

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields=['title','description','open_date','close_date','moderator','lesson_plan','active','prelims_test_series','mains_test_series']
    date_hierarchy = 'open_date'
    inlines=[PartInline]    


    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user            

        super().save_model(request, obj, form, change)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "moderator":            
            kwargs["queryset"] = User.objects.filter(groups__name='instructor')            

        return super(CourseAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "prelims_test_series":
            if request.user.is_superuser:                
                kwargs["queryset"] = Series.objects.all()
            elif request.user.groups.filter(name='Instructor').exists():               
                kwargs["queryset"] = Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))
        

        elif db_field.name == "prelims_test_series":

            if request.user.is_superuser:                
                kwargs["queryset"] = Mains_Test_Series.objects.all()
            elif request.user.groups.filter(name='Instructor').exists():               
                kwargs["queryset"] = Mains_Test_Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))
        

            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

            
    def save_formset(self, request, form, formset, change):        
        instances = formset.save(commit=False)
        for instance in instances:
            # Do something with `instance`
            instance.created_by = request.user
            instance.save()
        formset.save_m2m() 


    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(CourseAdmin, self).get_queryset(request)
        elif request.user.groups.filter(name='Instructor').exists():
            return Course.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))

           


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 0

    fields = ('name','subject', 'changeform_link')
    readonly_fields = ('changeform_link', )
    can_delete = False
    
    
class Live_SessionsInline(admin.TabularInline):
    model = Live_Sessions
    extra = 0 


class VideosInline(admin.TabularInline):
    model = Video
    extra = 0 


class MaterialInline(admin.TabularInline):
    model = Material
    extra = 0 

'''
class Class_TestInline(admin.TabularInline):
    model = Class_Test
    extra = 0 
    fields = ('title','part','description','class_changeform_link')
    readonly_fields = ('class_changeform_link', )
    can_delete = False
    
'''


class TestInline(admin.TabularInline):
    model = Test
    extra = 0
    fields = ('name','open_date','close_date', 'changeform_link',)
    readonly_fields = ('changeform_link', )
    can_delete = False


class MainsInline(admin.TabularInline):
    model = Assignment
    extra = 0
    fields = ('title', 'changeform_link',)
    readonly_fields = ('changeform_link', )
    can_delete = False



    

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    fields=['title','description','course','test_type']
    inlines=[TopicInline,TestInline,MainsInline]
    list_filter=['course']
    search_fields=['title']
    change_list_template = 'question_admin.html'
    change_form_template = "admin/question_upload.html"
    


    def save_formset(self, request, form, formset, change):        
        instances = formset.save(commit=False)
        for instance in instances:
            # Do something with `instance`
            instance.created_by = request.user
            instance.save()
        formset.save_m2m()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(PartAdmin, self).get_queryset(request)
        elif request.user.groups.filter(name='Instructor').exists():
            return Part.objects.filter(Q(course__created_by=request.user) | Q(course__moderator=request.user))

           

 


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    fields=['name','subject','part']
    inlines=[Live_SessionsInline,VideosInline,MaterialInline]
    list_filter=['part','subject','part__course']
    search_fields=['name']
    

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(TopicAdmin, self).get_queryset(request)
        elif request.user.groups.filter(name='Instructor').exists():
            return Topic.objects.filter(Q(part__course__created_by=request.user) | Q(part__course__moderator=request.user))



'''
@admin.register(Class_Test)
class Class_TestAdmin(admin.ModelAdmin):
    fields=['title','part','description']

    inlines=[TestInline]


    def save_formset(self, request, form, formset, change):        
        instances = formset.save(commit=False)
        for instance in instances:
            # Do something with `instance`
            instance.created_by = request.user
            instance.save()
        formset.save_m2m()

'''