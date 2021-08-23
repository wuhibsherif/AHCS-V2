from django.urls import path
from . import views


urlpatterns = [
    path('', views.nurse_homepage, name='nurse_homepage_url'),
    path('add_vital_sign/<str:pk>/', views.add_vital_sign, name="add_vital_sign_url"),
    path('admit_to_dr/<str:pk>/', views.admit_to_dr, name="admit_to_dr_url"),
    path('avaliable_physician/<str:value>/', views.find_available_physician, name="find_available_physician_url"),
    path('assign_doctor/', views.assign_doctor, name="assign_doctor_url"),
    path('assign_doctor/',views.assign_doctor,name="assign_doctor_url")
]
