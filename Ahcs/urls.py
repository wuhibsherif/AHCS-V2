"""Ahcs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', include('login.urls')),
                  ##  path('registration/',include('registration.urls')),
                  ##  path('accounts/',include('accounts.urls')),
                  ## path('reception/',include('reception.urls')),
                  path('physician/', include('physician.urls')),
                  path('radiologist/', include('radiologist.urls')),
                  path('lab_technician/', include('lab_technician.urls')),
                  path('pharmacist/', include('pharmacist.urls')),
                  path('hospital_admin/', include('hospital_admin.urls')),
                  path('pharmacy_admin/', include('pharmacy_admin.urls')),
                  path('receptionist/', include('receptionist.urls')),
                  path('nurse/', include('nurse.urls')),
                  path('admin/', admin.site.urls),
                  path('profiles/', include('profiles.urls')),
                  path('system_admin/', include('system_admin.urls')),
                  path('searches/', include('searches.urls')),

                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
