from django import forms
from assignment.models import Submission


class SubmissionForm(forms.ModelForm):  
    class Meta:
        model = Submission
        fields = ('sfile',)