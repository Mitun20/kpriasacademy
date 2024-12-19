from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url,include
from . import views as core_views

urlpatterns = [
     path('',core_views.CustomLoginView.as_view(), name='login',kwargs={'redirect_authenticated_user': True}),
     
     path('logout/',core_views.logout, name="student_logout"),
     path('edit_profile/',core_views.edit_profile, name="edit_profile"),
     path('home/',core_views.home, name="home"),
     path('dashboard/',core_views.dashboard, name="dashboard"),
     path('staff_dashboard/',core_views.dashboard_home,name='staff_dashboard'),
     path('staff_dashboard/test_series/<int:series_id>/',core_views.test_series_dashboard,name='test_series_dashboard'),
     path('ajax/load_dashboard/', core_views.draw_dashboard, name='ajax_load_dashboard'),
     path('ajax/load_dashboard_test/', core_views.draw_dashboard_test, name='ajax_load_dashboard_test'),
     path('question_upload/',core_views.question_upload, name="question_upload"),
     path('signup/',core_views.signup, name="signup"),
     path('registered/',core_views.registered, name="registered"),
     path('accounts/', include('django.contrib.auth.urls')),
     path('change_password/',core_views.change_password, name="change_password"),
     path('ajax/load-tests/', core_views.load_tests, name='ajax_load_tests'),
     path('ajax/load-course-tests/', core_views.load_course_tests, name='ajax_load_course_tests'),
     path('ajax/load-daily_mcq-tests/', core_views.load_daily_mcq_tests, name='ajax_load_daily_mcq_tests'),
     path('ajax/load-sholarship-tests/', core_views.load_sholarship_tests, name='ajax_load_scholarship_tests'),
     path('admin/logout/', lambda request: redirect('/logout/', permanent=False)),
     path('create_or_enroll/',core_views.EnrollmentView.as_view(),name='create_user'),
     path('contact_us/',core_views.contact_us, name="contact_us"),
     path('course_enrolment_batch_update/<int:course_enrolment_id>/',core_views.course_enrolment_batch_update,name='course_enrolment_batch_update'),
     path('print_pdf/<int:pk>/',core_views.print_pdf,name='print_pdf'),
     path('batch_update/',core_views.batch_update,name='batch_update'),
     path('view_profile/',core_views.view_profile,name='view_profile'),


     path('enquiry_submit/',core_views.EnquiryView.as_view(),name='enquiry'),
   
]