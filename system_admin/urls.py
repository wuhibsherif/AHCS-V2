from django.urls import path
from . import views

urlpatterns = [

    path('', views.homepage, name='system_admin_homepage_url'),
    path('add_new_healthcare_provider/', views.add_new_healthcare_provider, name='add_new_healthcare_provider_url'),
    path('manage_hospitals/',views.manage_hosptials,name="manage_hospitals_url"),
    path('manage_pharmacy/',views.manage_pharmacy,name="manage_pharmacy_url"),
    path('view_hospital_admins/', views.view_hospital_admins, name='view_hospital_admins_url'),
    path('view_pharmacy_admins/', views.view_pharmacy_admins, name='view_pharmacy_admins_url'),
    path('delete_hospital/<str:pk>/',views.delete_hospital,name='delete_hospital_url'),
    path('delete_pharmacy/<str:pk>/',views.delete_pharamcy,name='delete_pharmacy_url'),
    path('hospital_detail/<str:pk>/',views.hospital_detail,name='hospital_detail_url'),

]