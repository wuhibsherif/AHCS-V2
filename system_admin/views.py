from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.models import *
# Create your views here.
from hospital_admin.forms import UserRegistrationForm
from login import decorators
from pharmacist.models import Pharmacist
from system_admin.forms import HealthCareProviderRegistrationForm, Deletion_Form
from django.contrib import messages
from . import signals
@login_required(login_url='login_url')

def homepage(request):
    context = {}

    return render(request, 'system_admin/homepage.html', context)

@login_required(login_url='login_url')

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
            messages.success(request,"Health Care Provider Registered Successfully")
            return redirect('add_new_healthcare_provider_url')
    else:
        form = HealthCareProviderRegistrationForm
        form1 = UserRegistrationForm
    context = {'form': form, 'form1': form1}
    return render(request, 'system_admin/healthcare_provider_add.html', context)

@login_required(login_url='login_url')

def view_hospital_admins(request):
    hospital = Hospital.objects.all().exclude(is_active=False)
    context = {'hospital': hospital}
    return render(request, 'forms/all_hospital_admins.html', context)

@login_required(login_url='login_url')

def view_pharmacy_admins(request):
    pharmacy = Pharmacy.objects.all().exclude(is_active=False)


    context = {'pharmacy': pharmacy}
    return render(request, 'forms/all_pharmacy_admins.html', context)


def manage_hosptials(request):
    hospital = Hospital.objects.all().exclude(is_active=False)
    context = {'hospital': hospital}
    return render(request, 'forms/all_hospitals.html', context)
def manage_pharmacy(request):
    pharmacy = Pharmacy.objects.all().exclude(is_active=False)
    context = {'pharmacy': pharmacy}
    return render(request, 'forms/all_pharmacy.html', context)

def delete_hospital(request,pk):
    hospital = Hospital.objects.get(id=pk)
    staff = Staff.objects.filter(hospital_id=hospital.id)
    if request.method=='POST':
        hospital.is_active = False
        hospital.save()
        for staff in staff:
          user=User.objects.get(id=staff.basic_id)
          user.is_active=False
          user.save()
        return redirect('manage_hospitals_url')
    context={'hospital':hospital}
    return render(request, 'forms/hospital_deletion_confirmation.html', context)

def delete_pharamcy(request,pk):
    pharmacy = Pharmacy.objects.get(id=pk)
    pharmacist = Pharmacist.objects.filter(pharmacy=pharmacy.id)

    if request.method=='POST':
        pharmacy.is_active = False
        pharmacy.save()
        for pharmacist in pharmacist:
          user=User.objects.get(id=pharmacist.basic_id)
          print(user)
          pharmacy_admin =User.objects.get(id=pharmacy.admin.id)
          print(pharmacy_admin)
          pharmacy_admin.is_active=False
          pharmacy_admin.save()
          user.is_active=False
          user.save()
        return redirect('manage_hospitals_url')
    context={'pharmacy':pharmacy}
    return render(request, 'forms/pharmacy_deletion_confirmation.html', context)
def hospital_detail(request,pk):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            admin_type = 'hospital admin'
            admin = Hospital.objects.get(id=pk).admin
            admin.is_active=False
            admin.save()
            form.update_admin(admin_type,pk)
            return redirect('manage_hospitals_url')
    else:
        form=UserRegistrationForm
    hospital=Hospital.objects.get(id=pk)
    context={'hospital':hospital,'form':form}
    return render(request,'forms/hospital_detail.html',context)

def pharmacy_detail(request,pk):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            admin_type = 'pharmacy admin'
            admin = Pharmacy.objects.get(id=pk).admin
            admin.is_active=False
            admin.save()
            form.update_admin(admin_type,pk)
            return redirect('manage_pharmacy_url')
    else:
        form=UserRegistrationForm
    pharmacy=Pharmacy.objects.get(id=pk)
    context={'pharmacy':pharmacy,"form":form}
    return render(request,'forms/pharmacy_detail.html',context)
