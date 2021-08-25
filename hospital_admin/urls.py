from django.urls import path 
from . import views


urlpatterns = [
    path('', views.hospital_admin_homepage,
         name="hospital_admin_homepage_url"),
    path('add_new_user/', views.add_new_user, name='add_new_user_url'),
    path('all_receptionists', views.all_receptionists, name="all_receptionists_url"),
    path('all_users', views.all_users, name="all_users_url"),
    path('all_physicians',views.all_physicians,name="all_physicians_url"),
    path('all_nurses',views.all_nurses,name="all_nurses_url"),
    path('all_radiologists/', views.all_radiologists, name="all_radiologists_url"),
    path('all_lab_technicians/',views.all_lab_technicians,name="all_lab_technicians_url"),
    path('delete_staff/<str:pk>/',views.delete_staff,name="delete_staff_url"),
    path('all_pharmacists/',views.all_pharmacists,name="all_pharmacists_url"),#path('user_profile/<str:pk>/',views.user_profile,name="user_profile_url"),
    path('view_log/',views.view_log,name='view_log_url')




]
