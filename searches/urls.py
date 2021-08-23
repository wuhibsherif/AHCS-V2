from . import views
from django.urls import path

urlpatterns = [
    path('search_staff/', views.search_staff, name='search_staff_url'),
    path('search_nurse/', views.search_nurse, name='search_nurse_url'),
    path('search_physician/', views.search_physician, name='search_physician_url'),
    path('search_radiologist/', views.search_radiologist, name='search_radiologist_url'),
    path('search_lab_technician/', views.search_lab_technician, name='search_lab_technician_url'),
    path('search_healthcare_provider/', views.search_healthcare_provider, name='search_healthcare_provider_url'),
    path('search_patient/', views.search_patient, name='search_patient_url'),
    path('pharmacist_search_patient/', views.pharmacist_search_patient, name='pharmacist_search_patient_url'),
]
