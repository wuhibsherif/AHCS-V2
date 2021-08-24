from django.urls import path
from . import views


urlpatterns = [
    path('', views.admission_and_discharge_homepage, name='admission_and_discharge_homepage_url'),
    path('referral_from_other', views.referral_from_other_healthcare, name='referral_from_other_healthcare_url'),
    path('referral_from_internal', views.referral_from_internal, name='referral_from_internal_url'),
    path('referral_detail/<str:pk>/', views.referral_detail, name='referral_detail_url'),

]
