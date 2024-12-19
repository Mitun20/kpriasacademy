from django.contrib import admin
from .models import Mains_Test_Series
from account.models import User
from assignment.models import Assignment

# Register your models here.


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0
    fields = ('title', 'changeform_link',)
    readonly_fields = ('changeform_link', )



@admin.register(Mains_Test_Series)
class Mains_Test_SeriesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines=[AssignmentInline]
    fields=['title','description','start_date','end_date','moderator','lesson_plan','active']
    date_hierarchy = 'start_date'


    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:                 
            self.exclude = ('created_by', )         
            
        form = super(Mains_Test_SeriesAdmin, self).get_form(request, obj, **kwargs)
        return form

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "moderator":
            kwargs["queryset"] = User.objects.filter(groups__name='instructor')
        return super(Mains_Test_SeriesAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
            
            

           
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


           
          


