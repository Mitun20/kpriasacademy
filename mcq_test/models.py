from django.db import models
from django.contrib.auth.models import User
from tseries.models import Series
from subject.models import Subject
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils.safestring import mark_safe
from datetime import datetime, date, timedelta
from django import forms
from daily_mcq.models import Daily_Mcq
from course.models import Part
from subject.models import Subject
from scholarship.models import Scholarship_Test
from django.db.models import Max, Min, Avg, Count, Sum



class Question(models.Model):
    
    name=models.CharField(max_length=100)
    description=RichTextUploadingField(verbose_name="Question Statement")
    answer_description=RichTextUploadingField(blank=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    mark=models.FloatField(default=2)
    is_active=models.BooleanField(default=True,null=True)

    def __str__(self):
        return self.name

    def correct_option(self):
        correct = Option.objects.get(question__id=self.id,value=self.mark)
        return correct



    

class Option(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    description=RichTextUploadingField()
    value=models.FloatField(default=0)

    def alphabet(self):
        obj=Option.objects.get(id=self.id,question=self.question)
        alphabet = Option.objects.filter(id__lt=obj.id,question=self.question).count()

        if alphabet == 0:
            return "a"
        elif alphabet == 1:
            return "b" 
        elif alphabet == 2:
            return "c"
        elif alphabet == 3:
            return "d"
        else:
            return None
            
    class Meta:
        ordering = ['id']   


    

class Test(models.Model):
    name=models.CharField(max_length=30)
    description=RichTextUploadingField(null=True,blank=True)
    instruction=RichTextUploadingField(null=True,blank=True)
    open_date=models.DateTimeField()
    close_date=models.DateTimeField()
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='creator')    
    test_series=models.ForeignKey(Series,on_delete=models.CASCADE,null=True,blank=True)
    course_part=models.ForeignKey(Part,on_delete=models.CASCADE,null=True,blank=True)
    daily_mcq=models.OneToOneField(Daily_Mcq,on_delete=models.CASCADE,null=True,blank=True)
    scholarship_test=models.OneToOneField(Scholarship_Test,on_delete=models.CASCADE,null=True,blank=True)
    total_no_questions=models.PositiveIntegerField(null=True,blank=True)
    total_marks=models.FloatField(null=True,blank=True)
    duration_in_minutes=models.PositiveIntegerField(null=True,blank=True)
    question=models.ManyToManyField(Question,blank=True)
    show_answers=models.BooleanField(default=True)
    active=models.BooleanField(default=False)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    #allowed_attempts=models.PositiveIntegerField(null=True,blank=True)
    discussion_video_link=models.URLField(max_length=200,null=True,blank=True)
    negative_mark=models.BooleanField(default=True)
    live_discussion_link=models.URLField(max_length=200,null=True,blank=True)
    live_discussion_date=models.DateTimeField(null=True,blank=True)



    def __str__(self):
        return self.name

    @property
    def live_discussion_date_comparing(self):
        if self.live_discussion_date.date() >= date.today():
            return True
        else:
            return False

    def clean(self):       
       
        if self.close_date < self.open_date:
            raise forms.ValidationError("Close date should be greater than open date.")

    def changeform_link(self):
        if self.id:
            
            changeform_url = reverse(
            'admin:mcq_test_test_change', args=(self.id,)
            )
            return mark_safe(u'<a href="%s" target="_blank">View Test</a>' % changeform_url)
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = '' 

class On_Test(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test=models.ForeignKey(Test,on_delete=models.CASCADE)
    started_time=models.DateTimeField(null=True)
    
    
    class Meta:
        verbose_name = 'Live Test'
        verbose_name_plural = 'Live Test'



class Attempt(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test=models.ForeignKey(Test,on_delete=models.CASCADE)
    score=models.FloatField(default=0)
    start_date_time=models.DateTimeField()
    end_date_time=models.DateTimeField()



    def attempted_questions(self):
        attempted=Response.objects.filter(attempt=self.id,user=self.user).count()
        return str(attempted)

    def incorrect(self):
        incorrect=Response.objects.filter(attempt=self.id,user=self.user,option__value__lt=0).count()
        return str(incorrect)

    def correct(self):
        correct=Response.objects.filter(attempt=self.id,user=self.user,option__value__gt=0).count()
        return str(correct)

    def rank(self):
        obj=Attempt.objects.get(user=self.user,id=self.id,test=self.test)
        rank = Attempt.objects.filter(score__gt=obj.score,test=self.test).count()

        return rank+1

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def correct_score(self):
        correct=Response.objects.filter(attempt=self.id,user=self.user,option__value__gte=0).aggregate(Sum('option__value'))['option__value__sum']
        return str(correct)


    def net_score(self):
        if self.test.negative_mark:
            correct=Response.objects.filter(attempt=self.id,user=self.user,option__value__gte=0).aggregate(Sum('option__value'))['option__value__sum']
            incorrect=Response.objects.filter(attempt=self.id,user=self.user,option__value__lte=0).aggregate(Sum('option__value'))['option__value__sum']

            if correct is not None and incorrect is not None:
                net_score=correct+incorrect
                return str(round(net_score,2))
            elif correct is not None and incorrect is None:
                return str(round(correct,2))
            elif incorrect is not None:
                return str(round(incorrect,2))

        else:
            return self.score
            



    def duration(self):
        duration=self.end_date_time - self.start_date_time
        secs = duration.total_seconds()
       
        return int(secs / 60) % 60 


    @classmethod
    def Create(self,Testid,user,data,start_time):
        
        start_time=start_time        
        end_time=datetime.now()       
        
        test = Test.objects.get(id=Testid)
        attempt=self(user=user,test=test,start_date_time=start_time,end_date_time=end_time)
        attempt.save()
        objs = (Response(user=user,option=Option.objects.get(id=data[i]['optionid']),question=Question.objects.get(id=data[i]['questionid']),attempt=attempt) for i in range(len(data)))
        response = list(objs)
        Response.objects.bulk_create(response)
        
        
        mark=0     
        if test.negative_mark:
            print('negative test')
            for i in range(len(data)):
                question=Question.objects.get(id=data[i]['questionid'])
                option=Option.objects.get(id=data[i]['optionid'])
                mark=mark+option.value
                '''
                if question.mark == option.value:
                    mark=mark+(question.mark)                
                else:
                    minus_mark=minus_mark+(option.value)
                '''    
        else:
            for i in range(len(data)):
                question=Question.objects.get(id=data[i]['questionid'])
                option=Option.objects.get(id=data[i]['optionid'])
                if question.mark == option.value:
                    mark=mark+(question.mark)                
          

              
        mark=round(mark,2)
        Attempt.objects.filter(id=attempt.id).update(score=mark)
        On_Test.objects.filter(user=user,test=test.id).delete()
        
        return mark


    @classmethod
    def Mcq_Create(self,Testid,user,data,start_time):
        start_time=start_time
        end_time=datetime.now()    
            
        if user.is_anonymous:          
           
       
            mark=0   
            negative_mark=0   
            for i in range(len(data)):
                question=Question.objects.get(id=data[i]['questionid'])
                option=Option.objects.get(id=data[i]['optionid'])
          
                if question.mark == option.value:
                    mark=mark+(question.mark) 

                elif question.mark != option.value:
                    negative_mark=negative_mark+(option.value)                
                
            
            mark = mark+negative_mark
            negative_mark = negative_mark
            return mark,negative_mark           
                
              
        else:

            test = Test.objects.get(id=Testid)
            attempt=self(user=user,test=test,start_date_time=start_time,end_date_time=end_time)
            attempt.save()
            objs = (Response(user=user,option=Option.objects.get(id=data[i]['optionid']),question=Question.objects.get(id=data[i]['questionid']),attempt=attempt) for i in range(len(data)))
            response = list(objs)
            Response.objects.bulk_create(response)
       
            mark=0  
            negative_mark=0   
            for i in range(len(data)):
                question=Question.objects.get(id=data[i]['questionid'])
                option=Option.objects.get(id=data[i]['optionid'])
          
                if question.mark == option.value:
                    mark=mark+(question.mark) 

                elif question.mark != option.value:
                    negative_mark=negative_mark+(option.value)                
                
            mark = mark+negative_mark
            negative_mark = negative_mark            
            Attempt.objects.filter(id=attempt.id).update(score=mark)

            
            return mark,negative_mark



    def nagative_mark(self):
        mark=Response.objects.filter(attempt=self.id,user=self.user,option__value__lte=0).aggregate(Sum('option__value'))['option__value__sum']
    
        if mark is not None:
            return round(mark,2)


class Response(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attempt=models.ForeignKey(Attempt,on_delete=models.CASCADE)
    option=models.ForeignKey(Option,on_delete=models.CASCADE)  
    question=models.ForeignKey(Question,on_delete=models.CASCADE)


    def user_name(self):
        return self.user.first_name