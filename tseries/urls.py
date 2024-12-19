from django.urls import path
from . import views

urlpatterns = [
    path('test_series/',views.test_series_list,name="test_series"),
    path('my_test_series/',views.my_test_series_list,name="my_test_series"),
    path('test_series_performance/<int:pk>',views.series_performance,name='series_performance'),
    path('test_rank/<int:test>',views.test_rank,name='test_rank'),
    path('ajax/ajax_load_test/', views.ajax_load_test, name='ajax_load_test'),
    path('ajax/ajax_load_subject/', views.ajax_load_subject, name='ajax_load_subject'),
    path('ajax/ajax_load_mpm_test/', views.ajax_load_mpm_test, name='ajax_load_mpm_test'),
    path('ajax/ajax_load_pm_test/', views.ajax_load_pm_test, name='ajax_load_pm_test'),
    path('ajax/ajax_load_ysc_test/', views.ajax_load_ysc_test, name='ajax_load_ysc_test'),
    path('ajax/ajax_load_apm_csat_test/', views.ajax_load_apm_csat_test, name='ajax_load_apm_csat_test'),
    path('ajax/ajax_load_mpm_csat_test/', views.ajax_load_mpm_csat_test, name='ajax_load_mpm_csat_test'),
    path('ajax/ajax_load_cwt_csat_test/', views.ajax_load_cwt_csat_test, name='ajax_load_cwt_csat_test'),
    

   
    
]