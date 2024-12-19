from django.contrib import admin
from .models import Daily_Mcq
from mcq_test.models import Test,Question
from django.contrib.auth.models import User
from account.models import User
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db.models import Sum



# Register your models here.



class TestFormSet(BaseInlineFormSet):
    '''
    Validate formset data here
    '''
    def clean(self):
        super(TestFormSet, self).clean()
        
        
        correct_answer_count = 0
        non_zero_count = 0
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue   


            if form.cleaned_data['active']:
                if form.cleaned_data['total_no_questions'] != len(form.cleaned_data['question']):
                    raise ValidationError('Total No of Questions and choosed questions not matched ')


                if form.cleaned_data['total_marks'] != Question.objects.filter(id__in=form.cleaned_data['question']).aggregate(Sum('mark'))['mark__sum']:
                    raise ValidationError('Marks not matched ')



            

class TestInline(admin.TabularInline):
    model = Test
    extra = 0
    fields = ('name','open_date','close_date', 'changeform_link',)
    readonly_fields = ('changeform_link', )

 

@admin.register(Daily_Mcq)
class Daily_McqAdmin(admin.ModelAdmin):
    inlines=[TestInline]
    fields=['title','description','date']
    date_hierarchy = 'date'
    search_fields= ['title',]
    change_list_template = 'question_admin.html'
    change_form_template = "admin/question_upload.html"

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "moderator":
            kwargs["queryset"] = User.objects.filter(groups__name='Instructor').exclude(username=request.user.username)
        return super(Daily_McqAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
            

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user            

        super().save_model(request, obj, form, change)
        

    def save_formset(self, request, form, formset, change):        
        instances = formset.save(commit=False)
        for instance in instances:
            # Do something with `instance`
            instance.created_by = request.user
            instance.save()
        formset.save_m2m()


    def get_queryset(self, request):           
         
          if request.user.is_superuser:
              return super(Daily_McqAdmin, self).get_queryset(request)

          elif request.user.groups.filter(name='Super_Staff').exists():
              return Daily_Mcq.objects.filter(created_by=request.user)