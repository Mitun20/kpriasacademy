from django.urls import path
from . import views
from .views import testsubmit ,delete_on_test


urlpatterns = [
   
    path('test_series_detail/<int:series>/',views.test_series_detail,name='test_series_detail'),    
    path('view_instruction/<int:test>/',views.view_instruction,name='view_instruction'),
    path('test/<int:test>/',views.test,name='test'),
    path('quizdetail/',testsubmit),
    path('delete_on_test/',delete_on_test),
    path('delete_on_test/<int:test>/',views.delete_on_test,name='delete_on_test'),
    path('view_result/<int:test>/',views.view_result,name='view_result'),
    path('view_answer/<int:test>/',views.view_answer,name='view_answer'),
    path('test_completed/<int:test>/',views.test_completed,name='test_completed'),
    path('discussion/<int:test>/',views.view_discussion,name='discussion'),
    path('load_question/',views.load_question,name='load_question'),
    path('ajax_load_questions/',views.ajax_load_questions,name='ajax_load_questions'),
    
    
]
