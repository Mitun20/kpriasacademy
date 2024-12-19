from django import forms
from assignment.models import Submission,SFile


class SubmissionForm(forms.ModelForm):  
    class Meta:
        model = Submission
        fields = ()

class SForm(forms.ModelForm):
    sfile = forms.FileField(required=False,label='Select a file') 
    
    class Meta:
        model = SFile
        fields = ('sfile',)
