from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

from django.forms.widgets import PasswordInput, TextInput
from . models import User, Educational_Qualification, Family_Details
from django.forms.models import inlineformset_factory

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))
    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Custom error'
        super().__init__(*args, **kwargs)


        
class Educational_QualificationForm(forms.ModelForm):
    class Meta:
        model = Educational_Qualification
        fields = ('std','course','percentage','institution','place','year')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["std"].choices = [("", "Choose Standard"),] + \
            list(self.fields["std"].choices)[1:]
        



class Family_DetailsForm(forms.ModelForm):
    class Meta:
        model = Family_Details
        fields = ('name','relation','age','occupation','company','salary')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["relation"].choices = [("", "Choose Relation"),] + \
            list(self.fields["relation"].choices)[1:]
        


class EditUserForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date','placeholder':'DOB'} ) )
    signature_of_the_applicant=forms.FileField(required=False,widget=forms.FileInput(attrs={'accept':'image/x-png,image/jpg,image/jpeg,image/bmp'}))
    profile_picture=forms.ImageField(widget=forms.FileInput(attrs={'accept':'image/x-png,image/jpg,image/jpeg,image/bmp'}))


    class Meta:
        model = User
        fields = ('first_name','last_name','native','dob','community','religion','mother_tongue','mobile_no','present_address','permanent_address','age','gender','count_of_cleared_prelims_exam','count_of_cleared_mains_exam','count_of_cleared_interview','parents_mobile_no','profile_picture','signature_of_the_applicant',)
        
        required = ('first_name','last_name','native','dob','age','permanent_address','community','mother_tongue','religion','present_address','permanent_address','mobile_no','age','highest_qualification','parents_mobile_no','college_work','profile_picture','signature_of_the_applicant')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['mobile_no'].required = True
        
        self.fields['first_name'].required = True
        
        self.fields['last_name'].required = True

        self.fields['age'].required = True

        self.fields['community'].required = True   

        self.fields['religion'].required = True

        self.fields['mother_tongue'].required = True

        self.fields['parents_mobile_no'].required = True
     
        self.fields['present_address'].required = True     

        self.fields['permanent_address'].required = True        
        
        self.fields['native'].required = True

        self.fields['profile_picture'].required = True

        self.fields['signature_of_the_applicant'].required = True
        self.fields['gender'].required = True
       
    
     
EducationFormSet = inlineformset_factory(User, Educational_Qualification,
                                            form=Educational_QualificationForm, min_num=3, validate_min=True, extra=1,can_delete=False)



FamilyFormSet = inlineformset_factory(User, Family_Details,
                                            form=Family_DetailsForm, min_num=1, validate_min=True, extra=2,can_delete=False)




class SignupForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email','mobile_no','interview_quidance','daf')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mobile_no'].required = True
        self.fields['first_name'].required = True