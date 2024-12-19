from django.urls import path
from .import views

urlpatterns = [
    path('scholarship/',views.scholarship,name="scholarship"),
    path('scholarship_test/<int:test>/',views.test,name='scholarship_test'),
    path('scholarship_test_submission',views.scholarship_test_submission,name="scholarship_test_submission"),
    
]
