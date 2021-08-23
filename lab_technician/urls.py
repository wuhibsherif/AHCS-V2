from django.urls import path
from . import views


urlpatterns = [
    path('', views.lab_technician_homepage, name='lab_technician_homepage_url'),
    path('view_lab_request_detail/<str:pk>/', views.view_lab_request_detail, name='view_lab_request_detail_url'),
    path('add_stool_result/<str:pk>/', views.add_stool_result, name='add_stool_result_url'),
    path('add_urine_result/<str:pk>/', views.add_urine_result, name='add_urine_result_url'),
    path('add_hematology_result/<str:pk>/', views.add_hematology_result, name='add_hematology_result_url'),
    path('remove_from_labtechnician_list/<str:pk>/', views.remove_from_list, name='remove_from_labtechnician_list_url'),

]
