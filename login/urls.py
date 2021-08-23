from django.urls import path

from . import views

urlpatterns = [

    path('', views.user_login, name='login_url'),
    path('logout/', views.user_logout, name="user_logout_url")
]
