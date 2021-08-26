from django.urls import path
from . import views


urlpatterns =[
    path('check/<str:username>/<str:password>/',views.check),
    path('get_medications/<str:username>/',views.getMedication),
    path('get_appointment/<str:username>/', views.getAppointment),
]