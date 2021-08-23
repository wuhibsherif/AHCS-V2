from django.urls import path
from . import views


urlpatterns = [
    path('', views.receptionist_dashboard, name='receptionist_homepage_url'),
    path('registration/', views.register_new_patient, name='register_new_patient_url'),
    path('patient_profile/<str:pk>/', views.patient_profile, name='patient_profile_url'),
    path('admit_to_triage/<str:pk>/', views.admit_to_triage, name='admit_to_triage_url'),

    #path('my_profile/<str:pk>/', views.receptionist_profile, name='receptionist_profile_url')


    
    
    
    
]
