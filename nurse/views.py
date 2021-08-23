import json
from datetime import datetime

from django.db.models import Count, Min
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from accounts.models import Staff, User, Hospital
from login import decorators, urls
from login.decorators import allowed_users
from login.views import user_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required(login_url='login_url')
# @decorators.nurseonly
from patient.forms import VitalSignForm
from patient.models import Patient
from physician.models import PatientWaitingList
from receptionist.models import Triage

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Nurse'])
def nurse_homepage(request):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    request.session['healthcare_name'] = hospital.name
    try:
        triage_list = Triage.objects.filter(hospital_id=Staff.objects.get(basic_id=request.user.id).hospital_id,
                                            status='pending')
        triage = True
        context = {'triage': triage, 'triage_list': triage_list}
        return render(request, "nurse/homepage.html", context)
    except:
        triage = False
        context = {'triage': triage}
        return render(request, "nurse/homepage.html", context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Nurse'])
def add_vital_sign(request, pk):
    msg = 'successfully added'
    if request.method == 'POST':
        form = VitalSignForm(request.POST)
        patient = Patient.objects.get(basic_id=pk)
        staff = Staff.objects.get(basic_id=request.user.id)
        hospital = staff.hospital
        context = {'patient': patient, 'staff': staff, 'hospital': hospital}
        if form.is_valid():
            form.save_vital_sign(context)
            # nxt = request.POST.get('next', '/')
            return redirect('admit_to_dr_url', pk)
        else:
            form = VitalSignForm
            patient = User.objects.get(id=pk)
            context = {'form': form, 'patient': patient}
            return render(request, "nurse/form/vital_sign_form.html", context)

    else:
        form = VitalSignForm
        patient = User.objects.get(id=pk)
        context = {'form': form, 'patient': patient}
        return render(request, "nurse/form/vital_sign_form.html", context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Nurse'])
def admit_to_dr(request, pk):
    distinct = Staff.objects.filter(hospital_id=Staff.objects.get(basic_id=request.user.id).
                                    hospital_id).values('specialty').exclude(specialty=None).distinct()

    form = VitalSignForm
    patient = User.objects.get(id=pk)
    context = {'form': form, 'patient': patient, 'distinct': distinct}
    return render(request, "nurse/form/admit_to_dr.html", context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Nurse'])
def find_available_physician(request, value):
    """free_dr = PatientWaitingList.objects.filter(hospital_id=Staff.objects.get(basic_id=request.user.id).hospital_id,
                                            physician_speciality=value, status='pending').annotate(
        num_waiting=Count('physician_id')).order_by('num_waiting')"""
    hospital_id = Staff.objects.get(basic_id=request.user.id).hospital_id
    free_dr = Staff.objects.filter(hospital_id=hospital_id, specialty=value).order_by('-num_waiting').last().basic
    return HttpResponse(free_dr)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Nurse'])
def assign_doctor(request):
    doctor = request.POST['doctor']
    patient = request.POST['patient']
    waiting_list = PatientWaitingList.objects.create(
        hospital_id=Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id).id,
        physician_id=Staff.objects.get(basic_id=User.objects.get(username=doctor)).id,
        physician_speciality=Staff.objects.get(basic_id=User.objects.get(username=doctor)).specialty,
        patient_id=Patient.objects.get(basic_id=User.objects.get(id=patient)).id,
        added_by_id=Staff.objects.get(basic_id=request.user.id).id,
        status='pending',
    )
    waiting_list.save()
    staff = Staff.objects.get(basic_id=User.objects.get(username=doctor).id)
    staff.num_waiting = staff.num_waiting + 1
    staff.save()
    triage = Triage.objects.get(patient_id=Patient.objects.get(basic_id=patient), hospital_id=staff.hospital_id, status='pending')
    triage.status = 'approved'
    triage.save()
    return redirect('nurse_homepage_url')
