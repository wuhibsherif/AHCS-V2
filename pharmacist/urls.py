from django.urls import path
from . import views


urlpatterns = [
    path('', views.pharmacist_homepage, name='pharmacist_homepage_url'),
    path('add_medication_detail/<str:pk>/<str:pk2>/', views.add_medication_details, name='add_medication_details_url'),
    path('authenticate_patient/', views.authenticate_patient, name='authenticate_patient_url'),
    path('prescription_detail/<str:pk>/', views.prescription_detail, name='prescription_detail_url'),

]
