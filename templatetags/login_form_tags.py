from django.template import Library
 
register = Library()
 
@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class':'form-control form-control-solid h-auto py-5 px-6'})


 
@register.filter(name='addclass_profile')
def addclass_profile(field, class_attr):
    return field.as_widget(attrs={'class':'form-control  '})
