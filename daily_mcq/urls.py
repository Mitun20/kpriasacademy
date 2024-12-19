from django.urls import path
from . import views
from django.conf.urls import url
from .views import mcqtestsubmit 

urlpatterns = [

    path('daily_mcq/',views.daily_mcq_list,name="daily_mcq"),
    path('daily_mcq_test/<int:test>/',views.test,name='mcq_test'),
    path('daily_mcq/<int:year>/',views.year_by_daily_mcq,name='daily_mcq_year'),
    path('mcqtest/',mcqtestsubmit),
    path('daily_mcq_answer/<int:test>/',views.daily_mcq_answer,name='daily_mcq_answer'),  
    url(r'^daily_mcq/(?P<month>\w+)/(?P<year>\w+)/$', views.daily_mcq_filter_by_month, name='daily_mcq_filter'),
]
