from django.contrib import admin
from .models import Scholarship_Test
from account.models import User
from mcq_test.models import Test,Question
from django.db.models import Q
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db.models import Sum



# Register your models here.


class TestInline(admin.TabularInline):
    model = Test
    extra = 0
    fields = ('name','open_date','close_date', 'changeform_link',)
    readonly_fields = ('changeform_link', )




@admin.register(Scholarship_Test)
class Scholarship_TestAdmin(admin.ModelAdmin):
    fields=['title','description','open_date','close_date','moderator','active']
    inlines=[TestInline]
    date_hierarchy='open_date'
    search_fields=['title']
    change_list_template = 'question_admin.html'
    change_form_template = "admin/question_upload.html"

    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user            

        super().save_model(request, obj, form, change)


    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "moderator":
            kwargs["queryset"] = User.objects.filter(groups__name='Super_Staff')
        return super(Scholarship_TestAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
            
    def save_formset(self, request, form, formset, change):        
        instances = formset.save(commit=False)
        for instance in instances:
            # Do something with `instance`
            instance.created_by = request.user
            instance.save()
        formset.save_m2m()

    def get_queryset(self, request):           
         
        if request.user.is_superuser:
            return super(Scholarship_TestAdmin, self).get_queryset(request)

        elif request.user.groups.filter(name='Instructor').exists():
            return Scholarship_Test.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))

           
        elif request.user.groups.filter(name='Super_staff').exists():
            return Scholarship_Test.objects.filter(Q(created_by=request.user) | Q(moderator=request.user))