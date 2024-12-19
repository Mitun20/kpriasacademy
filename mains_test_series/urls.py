from django.urls import path,include
from . import views

urlpatterns = [
    path('mains_test_series/',views.mains_test_series_list,name="mains_test_series"),
    path('mains_test_series_detail/<int:series>/',views.mains_test_series_detail,name='mains_test_series_detail'),    
    path('mains_test_reslt/<int:assignment_id>/',views.mains_test_result,name='mains_test_result'),    
    path('mains_test/<int:assignment_id>/',views.mains_test,name='mains_test'), 
    path('mains_performance/<int:pk>',views.mains_performance,name='mains_performance'),   

    
]