from django.urls import path
from . import views

urlpatterns = [
    path('course/',views.course_list,name="course"),
    path('my_course',views.my_course_list,name="my_course"),
    path('course_detail/<int:course>/',views.course_detail,name='course_detail'),
    path('material/<int:part>/',views.material,name='material'),
    path('video/<int:part>/',views.video,name='video'),
    path('session/<int:part>/<int:course>',views.session,name='session'),
    path('course_test_list/<int:part>/',views.test_list,name='test_list'),
    path('course_test/<int:test>/',views.test,name='course_test'),
    path('course_view_result/<int:test>/',views.view_result,name='course_view_result'),
    path('course_test_answer/<int:test>/',views.view_answer,name='course_test_answer'),   
    path('course_mains_test/',views.course_mains_test,name='course_mains_test'),
    
    path('course_mains_part_test/<int:part>/',views.course_mains_part_test,name='course_mains_part_test'), 
    
    #path('course_mains_test_detail/<int:course>/',views.course_mains_test_detail,name='course_mains_test_detail'), 
    path('course_mains_test/<int:assignment_id>/',views.course_mains_test,name='course_mains_test'), 
    path('course_mains_test_reslt/<int:assignment_id>/',views.course_mains_test_result,name='course_mains_test_result'),    
    path('course_load_question/',views.load_question,name='course_load_question'),
    path('course_performance/<int:pk>',views.course_performance,name='course_performance'), 
    path('course_schedule/<int:course_id>/',views.schedule,name='course_schedule'),

]