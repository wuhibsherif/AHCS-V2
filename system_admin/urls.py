from django.urls import path
from . import views

urlpatterns = [

    path('', views.homepage, name='system_admin_homepage_url'),
    path('add_new_healthcare_provider/', views.add_new_healthcare_provider, name='add_new_healthcare_provider_url'),
    path('view_hospital_admins/', views.view_hospital_admins, name='view_hospital_admins_url'),
    path('view_pharmacy_admins/', views.view_pharmacy_admins, name='view_pharmacy_admins_url'),

]