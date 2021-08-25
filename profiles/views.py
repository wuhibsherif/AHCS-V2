from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.models import User
from hospital_admin.forms import *

# Create your views here.
from login.decorators import allowed_users
from profiles.forms import PasswordForm, Update_user_profile, update_user_address


@login_required(login_url='login_url')
def user_profile(request, pk):
    profile = User.objects.get(id=pk)
    print(profile)
    found = 'True'
    context = {'found': found, 'user_profile': profile}
    if request.user.is_superuser:
        return render(request, 'profiles/system_admin_users_profile.html', context)
    elif request.user.role == 'hospital admin':
        return render(request, 'profiles/hospital_admin_users_profile.html', context)
    elif request.user.role == 'pharmacy admin':
        return render(request, 'profiles/system_admin_users_profile.html', context)
    elif request.user.role == 'Physician':
        return render(request, 'profiles/system_admin_users_profile.html', context)
    elif request.user.role == 'Receptionist':
        return render(request, 'profiles/system_admin_users_profile.html', context)
    elif request.user.role == 'Nurse':
        return render(request, 'profiles/system_admin_users_profile.html', context)
    elif request.user.role == 'Lab Technician admin':
        return render(request, 'profiles/system_admin_users_profile.html', context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Receptionist', 'pharmacist', 'Physician', 'pharmacy admin', 'hospital admin', 'Radiologist', 'Admission and discharge', 'Nurse', 'pharmacy admin', 'Lab_technician'])
def my_profile(request, pk):
    username=request.user.username
    if request.method=="POST":
        form1=PasswordForm(request.POST)
        form=Update_user_profile(request.POST,instance=request.user)
        form2=update_user_address(request.POST,instance=request.user.address)
        if form1.is_valid():
            print(" valid")
            form1.update_password(username)

            return redirect('my_profile_url',pk)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
    else:
        form1 = PasswordForm()
        form = Update_user_profile(instance=request.user)
        form2 = update_user_address(instance=request.user.address)
    profile = User.objects.get(id=pk)
    role = request.user.role
    context = {'user_profile': profile,'form':form,'role': role,'form1':form1,'form2':form2}
    print(role)
    if request.user.is_superuser:
        return render(request, 'profiles/system_admin_my_profile.html', context)
    elif role == 'hospital admin':
        return render(request, 'profiles/hospital_admin_my_profile.html', context)
    elif role == 'pharmacy admin':
        return render(request, 'profiles/pharmacy_admin_my_profile.html', context)
    elif role == 'pharmacist':
        return render(request, 'profiles/pharmacist_my_profile.html', context)
    elif role == 'Physician':
        return render(request, 'profiles/physician_my_profile.html', context)
    elif role == 'Receptionist':
        return render(request, 'profiles/receptionist_my_profile.html', context)
    elif role == 'Radiologist':
        return render(request, 'profiles/radiologist_my_profile.html', context)
    elif role == 'Admission and discharge':
        return render(request, 'profiles/admission_and_discharge_my_profile.html', context)
    elif role == 'Lab_technician':
        return render(request, 'profiles/lab_technician_my_profile.html', context)
    elif role == 'Nurse':
        return render(request, 'profiles/nurse_my_profile.html', context)
