from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.models import *
# Create your views here.
from hospital_admin.forms import UserRegistrationForm
from login import decorators
from system_admin.forms import HealthCareProviderRegistrationForm
from django.contrib import messages

@login_required(login_url='login_url')
@decorators.allowed_users(allowed_roles=['system admin'])
def homepage(request):
    context = {}

    return render(request, 'system_admin/homepage.html', context)

@login_required(login_url='login_url')
@decorators.allowed_users(allowed_roles=['system admin'])
def add_new_healthcare_provider(request):
    msg = None
    if request.method == 'POST':
        form = HealthCareProviderRegistrationForm(request.POST)
        form1 = UserRegistrationForm(request.POST)
        print(form1.errors)
        if form1.is_valid() and form.is_valid():
            print(form.cleaned_data.get('type'))
            if form.cleaned_data.get('type') == 'Pharmacy':
                admin_type = 'pharmacy admin'
            else:
                admin_type = 'hospital admin'
            admin = form1.save_admin(admin_type)
            form.save_healthcare_provider(admin["admin_id"])
            messages.success(request,"Health Care Provider Registered Succesfully")
            return redirect('add_new_healthcare_provider_url')
    else:
        form = HealthCareProviderRegistrationForm
        form1 = UserRegistrationForm
    context = {'form': form, 'form1': form1}
    return render(request, 'system_admin/healthcare_provider_add.html', context)

@login_required(login_url='login_url')
@decorators.allowed_users(allowed_roles=['system admin'])
def view_hospital_admins(request):
    hospital = Hospital.objects.all()
    context = {'hospital': hospital}
    return render(request, 'forms/all_hospital_admins.html', context)

@login_required(login_url='login_url')
@decorators.allowed_users(allowed_roles=['system admin'])
def view_pharmacy_admins(request):
    pharmacy = Pharmacy.objects.all()
    context = {'pharmacy': pharmacy}
    return render(request, 'forms/all_pharmacy_admins.html', context)
