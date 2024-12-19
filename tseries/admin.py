from django.contrib import admin
from .models import Series
from mcq_test.models import Test
from django.contrib.auth.models import User
from account.models import User
from django import forms
from django.db.models import Q
from assignment.models import Assignment

# Register your models here.



class TestInline(admin.TabularInline):
    model = Test
    extra = 0
    fields = ('name','open_date','close_date', 'changeform_link',)
    readonly_fields = ('changeform_link', )




class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0
    fields = ('title', 'changeform_link',)
    readonly_fields = ('changeform_link', )


    


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines=[TestInline]
    fields=['title','description','start_date','end_date','moderator','lesson_plan','active']
    date_hierarchy = 'start_date'
    list_filter = ['active',]
    search_fields = ['title',]
    change_list_template = 'question_admin.html'
    change_form_template = "admin/question_upload.html"


    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:                 
            self.exclude = ('created_by', )         
            
        form = super(SeriesAdmin, self).get_form(request, obj, **kwargs)
        return form

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "moderator":
            kwargs["queryset"] = User.objects.filter(groups__name='Instructor')
        return super(SeriesAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
            
            

           
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user            

        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):        
        instances = formset.save(commit=False)
        for instance in instances:
            instance.created_by = request.user
            instance.save()
        formset.save_m2m()

    def get_queryset(self, request):           
         
          if request.user.is_superuser:
              return super(SeriesAdmin, self).get_queryset(request)

          elif request.user.groups.filter(name='Instructor').exists():
              return Series.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))

           
          








          '''
          if request.user.is_superuser:
              return Topic.objects.all()
          elif request.user.groups.filter(name='School').exists():
              if croomid:
                  return Topic.objects.filter(croom__school=request.user.school,croom=croomid,croom__board=request.user.school.board)
              else:
                  return Topic.objects.filter(croom__school=request.user.school,croom__board=request.user.school.board)    
             
              
          elif request.user.groups.filter(name='Teacher').exists():
              if croomid:
                  return Topic.objects.filter(croom__created_by=request.user,croom=croomid)
              else:
                  return Topic.objects.filter(croom__created_by=request.user)
          '''