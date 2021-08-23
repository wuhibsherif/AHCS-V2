from django.urls import path 
from . import views


urlpatterns = [
    path('', views.pharmacy_admin_homepage, name="pharmacy_admin_homepage_url"),
    path('register_new_pharmacist/', views.register_pharmacist, name='register_new_pharmacist_url'),
    path('all_pharmacists/', views.all_pharmacists, name="all_pharmacists_url"),
]
