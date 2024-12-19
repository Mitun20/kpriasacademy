from django.urls import path,include
from . import views

urlpatterns = [
    path('mains_course',views.mains_course_list,name="mains_course"),
    path('mains_course_detail/<int:series>/',views.mains_course_detail,name='mains_course_detail'),    
    path('course_mains_test_reslt/<int:assignment_id>/',views.course_mains_test_result,name='course_mains_test_result'),    
    path('course_mains_test/<int:assignment_id>/',views.course_mains_test,name='course_mains_test'),    

    
]


