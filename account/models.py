from __future__ import unicode_literals
import email
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from django.contrib.auth.models import Group
from mcq_test.models import Series
from course.models import Course,Batch
from scholarship.models import Scholarship_Test
from mains_test_series.models import Mains_Test_Series
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.db.models import Sum
import datetime


upse_status_options = (('','Choose Current Status of UPSC'),('Student','Student'),('Prelims Attempted','Prelims Attempted'),('Prelims Qualified','Prelims Qualified'),('Mains Attempted','Mains Attempted'),('Mains Qualified','Mains Qualified'))

gender_options = (('','Choose Gender'),('M','Male'),('F','Female'))
fee_type = (('','Choose Fee Type'),('H','Hostel Fee'),('S','Study Hall Fee'))
duration_type = (('','Choose Duration Type'),('6','Six Month'),('12','One Year'))

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(_('email address'),unique=True )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)       
    father_name=models.CharField(max_length=30,blank=True,null=True)
    present_address=models.TextField(blank=True,null=True)
    mobile_no=models.CharField(max_length=10,blank=True,null=True)
    highest_qualification=models.CharField(max_length=50,blank=True,null=True,verbose_name="Educational Qualification")
    current_status_upsc=models.CharField(choices=upse_status_options,max_length=20,blank=True,null=True)
    is_lateral = models.BooleanField(default=False,blank=True,null=False)
    profile_picture=models.ImageField(blank=True,null=True,upload_to='profile_photo')
    registered_on=models.DateField(auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True) 
    is_staff=models.BooleanField(default=False)
    groups=models.ManyToManyField(Group)
    test_series=models.ManyToManyField(Series, through='Test_Series_Enrolment')   
    
    

    admission_number=models.CharField(max_length=20,null=True,blank=True)
    age=models.PositiveIntegerField(null=True,blank=True)
    native=models.CharField(max_length=30,null=True,blank=True)
    parents_mobile_no=models.CharField(max_length=10,blank=True,null=True)
    batch=models.CharField(max_length=10,null=True,blank=True)
    college_work=models.CharField(max_length=100,null=True,blank=True)
    mode=models.CharField(max_length=30,null=True,blank=True)
    organization_fees=models.CharField(max_length=30,null=True,blank=True)
    scholarship=models.CharField(max_length=30,null=True,blank=True)
    academic=models.CharField(max_length=15,null=True,blank=True)
    hostel=models.CharField(max_length=15,null=True,blank=True)
    ttl=models.CharField(max_length=15,null=True,blank=True)
    admission_fees=models.CharField(max_length=15,null=True,blank=True)
    gst=models.CharField(max_length=15,null=True,blank=True)
    mode_of_payment=models.CharField(max_length=15,null=True,blank=True)

    age=models.PositiveIntegerField(null=True,blank=True)
    community=models.CharField(max_length=100,null=True,blank=True)
    religion=models.CharField(max_length=100,null=True,blank=True)
    mother_tongue=models.CharField(max_length=100,null=True,blank=True)
    signature_of_the_applicant=models.ImageField(blank=True,null=True,upload_to='signature')
    permanent_address=models.TextField(blank=True,null=True)
    dob=models.DateField(null=True,blank=True)  
    once_submited=models.BooleanField(default=False,null=True,blank=True)
    count_of_cleared_prelims_exam=models.PositiveIntegerField(null=True,blank=True)
    count_of_cleared_mains_exam=models.PositiveIntegerField(null=True,blank=True)
    count_of_cleared_interview=models.PositiveIntegerField(null=True,blank=True)

    interview_quidance=models.BooleanField(default=False)
    daf=models.FileField(upload_to='daf', max_length=254,null=True,blank=True )

    gender=models.CharField(choices=gender_options,max_length=1,blank=True,null=True)
    academic_fees = models.CharField(max_length=10,null=True,blank=True)
    admission_fees = models.CharField(max_length=5,null=True,blank=True)
    under = models.CharField(max_length=50,null=True,blank=True)
    
    date = models.DateField(null=True,blank=True)
    regular = models.BooleanField(default=False)
    weekend = models.BooleanField(default=False)
    hostel = models.BooleanField(default=False)
    study_hall = models.BooleanField(default=False)
    merit = models.BooleanField(default=False)
    received_amount=models.CharField(max_length=30,null=True,blank=True)
    hostel_fees = models.CharField(max_length=30,null=True,blank=True)
    hostel_fees_paid_date=models.DateField(null=True,blank=True)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def degree(self):
        degree = Educational_Qualification.objects.filter(user=self).values_list('course',flat=True).order_by('-id').last()        
        if degree:
            return degree
        else:
            return ''



    def miscellaneous_fee(self):
        fee = Miscellaneous_Fee.objects.filter(user__email=self.email).aggregate(Sum('amount'))
        return fee['amount__sum']

    def course_facility(self):
        paid_for = list(Miscellaneous_Fee.objects.filter(user__email=self.email).values_list('paid_for',flat=True))
        return ", ".join(paid_for)

class STD(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Relation(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Educational_Qualification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.CharField(max_length=200,null=True,blank=True)
    std=models.ForeignKey(STD,on_delete=models.CASCADE)
    percentage=models.FloatField()
    institution=models.CharField(max_length=200)
    place=models.CharField(max_length=100)
    year=models.PositiveIntegerField()

class Family_Details(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    relation=models.ForeignKey(Relation,on_delete=models.CASCADE,null=True,blank=True)
    age=models.PositiveIntegerField(null=True,blank=True)
    occupation=models.CharField(max_length=50,null=True,blank=True)
    company=models.CharField(max_length=100,null=True,blank=True)
    salary=models.FloatField(null=True,blank=True)



class Test_Series_Enrolment(models.Model):
    series = models.ForeignKey(Series,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    joined_on = models.DateField()
    

    class Meta:
        verbose_name_plural = "Prelims Test Series Enrolment"

    def admission_number(self):
        return self.user.admission_number

class Mains_Test_Series_Enrolment(models.Model):
    series = models.ForeignKey(Mains_Test_Series,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    joined_on = models.DateField()
    

    class Meta:
        verbose_name_plural = "Mains Test Series Enrolment"

    def admission_number(self):
        return self.user.admission_number




class Course_Enrolment(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    joined_on = models.DateField()
    is_lateral = models.BooleanField(default=False)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        verbose_name_plural = "Course Enrolment"
        ordering = ('user__admission_number',)

    def admission_number(self):
        return self.user.admission_number

    def phone_no(self):
        return self.user.mobile_no

    def save(self, *args, **kwargs):
        course = Course.objects.get(id=self.course.id)
        
       
        if course.mains_test_series:                        
            series=Mains_Test_Series.objects.get(id=course.mains_test_series.id)
            if not Mains_Test_Series_Enrolment.objects.filter(series=series,user=self.user).exists():

                Mains_Test_Series_Enrolment.objects.create(user=self.user,series=series,joined_on=datetime.date.today())
                
                if course.prelims_test_series is not None:
                    series=Series.objects.get(id=course.prelims_test_series.id)
                    if not Test_Series_Enrolment.objects.filter(series=series,user=self.user).exists():
                        Test_Series_Enrolment.objects.create(user=self.user,series=series,joined_on=datetime.date.today())
            else:
                 if course.prelims_test_series is not None:
                    series=Series.objects.get(id=course.prelims_test_series.id)
                    if not Test_Series_Enrolment.objects.filter(series=series,user=self.user).exists():
                        Test_Series_Enrolment.objects.create(user=self.user,series=series,joined_on=datetime.date.today())


        elif course.prelims_test_series is not None:          
            series=Series.objects.get(id=course.prelims_test_series.id)
            if not Test_Series_Enrolment.objects.filter(series=series,user=self.user).exists():
                Test_Series_Enrolment.objects.create(user=self.user,series=series,joined_on=datetime.date.today())

        super(Course_Enrolment, self).save(*args, **kwargs)


class Scholarship_Test_Enrolment(models.Model):
    scholarship_test = models.ForeignKey(Scholarship_Test,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    joined_on = models.DateField()
    
    class Meta:
        verbose_name_plural = "Scholarship Test Enrolment"

    def admission_number(self):
        return self.user.admission_number

class Miscellaneous_Fee(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField(null=True,blank=True)
    paid_date = models.DateTimeField(auto_now=True)
    paid_for = models.TextField(null=True)

    def __str__(self):
        return str(self.user)


class Enquiry(models.Model):
    name = models.CharField(max_length=254)
    email= models.EmailField(max_length=254)
    mobile_number= models.CharField(max_length=20)
    alternate_mobile_number= models.CharField(max_length=20,null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = ('Enquirie')



