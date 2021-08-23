import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from accounts.models import Hospital, Staff
from lab_technician.forms import StoolResultForm, UrineResultForm, HematologyResultForm
from lab_technician.models import UrineAnalysisWaitingList, HematologyWaitingList
from login.decorators import allowed_users
from patient.models import Hematology, UrineAnalysis, StoolExamination, Patient

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Lab_technician'])
def lab_technician_homepage(request):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    staff = Staff.objects.get(basic_id=request.user.id)
    request.session['healthcare_name'] = hospital.name
    context = {}
    hematology = Hematology.objects.filter(hospital_id=hospital.id, requested_to_id=staff.id,
                                           status='pending')
    if hematology.all:
        context['hematology'] = hematology
    urine = UrineAnalysis.objects.filter(hospital_id=hospital.id, requested_to_id=staff.id,
                                         status='pending')
    if urine.all:
        context['urine'] = urine
    stool = StoolExamination.objects.filter(hospital_id=hospital.id, requested_to_id=staff.id,
                                            status='pending')
    if stool.all:
        context['stool'] = stool

    return render(request, 'lab_technician/homepage.html', context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Lab_technician'])
def view_lab_request_detail(request, pk):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    staff = Staff.objects.get(basic_id=request.user.id)
    context = {}
    instance ={'hospital': hospital.id, 'staff': staff.id, 'patient': pk}
    try:
        hematology = Hematology.objects.get(hospital_id=hospital.id, requested_to_id=staff.id, patient_id=pk,
                                            status='pending')
        context['hematology'] = hematology
        context["hematology_result_form"] = HematologyResultForm(instance=instance)
    except:
        not_found = True
    try:
        urine = UrineAnalysis.objects.get(hospital_id=hospital.id, requested_to_id=staff.id, patient_id=pk,
                                          status='pending')
        context['urine'] = urine
        context["urine_result_form"] = UrineResultForm(instance=instance)

    except:
        not_found = True
    try:
        stool = StoolExamination.objects.get(hospital_id=hospital.id, requested_to_id=staff.id, patient_id=pk,
                                             status='pending')
        context['stool'] = stool
        context["stool_result_form"] = StoolResultForm(instance=instance)

    except:
        not_found = True

    context['user_profile'] = Patient.objects.get(id=pk)
    return render(request, "lab_technician/form/view_request.html", context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Lab_technician'])
def add_stool_result(request, pk):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    staff = Staff.objects.get(basic_id=request.user.id)
    instance = {'hospital': hospital.id, 'staff': staff.id, 'patient': pk}
    if request.method == 'POST':
        stool = StoolResultForm(request.POST, instance=instance)
        staff = Staff.objects.get(basic_id=request.user.id)
        hospital = staff.hospital

        rqst = StoolExamination.objects.filter(hospital_id=hospital.id, requested_to_id=staff.id,
                                            patient_id=pk, status='pending').latest('date_of_request')

        if stool.is_valid():
            for s in stool:
                setattr(rqst, s.name, stool.cleaned_data.get(s.name))

            rqst.date_of_report = datetime.datetime.now()
            rqst.reported_by_id = staff.id
            rqst.status = 'reported'
            rqst.save()
            return redirect('view_lab_request_detail_url', pk)
        else:
            print(stool.errors)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Lab_technician'])
def add_urine_result(request, pk):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    staff = Staff.objects.get(basic_id=request.user.id)
    instance = {'hospital': hospital.id, 'staff': staff.id, 'patient': pk}
    if request.method == 'POST':
        urine = UrineResultForm(request.POST, instance=instance)
        staff = Staff.objects.get(basic_id=request.user.id)
        hospital = staff.hospital

        rqst = UrineAnalysis.objects.filter(hospital_id=hospital.id, requested_to_id=staff.id,
                                         patient_id=pk, status='pending').latest('date_of_request')
        waiting = UrineAnalysisWaitingList.objects.filter(hospital_id=hospital.id, requested_to_id=staff.id,
                                                       patient_id=pk, status='pending').latest('date_of_request')

        if urine.is_valid():
            for s in urine:
                setattr(rqst, s.name, urine.cleaned_data.get(s.name))

            rqst.date_of_report = datetime.datetime.now()
            rqst.reported_by_id = staff.id
            rqst.status = 'reported'
            rqst.save()
            waiting.status = 'reported'
            waiting.save()
            return redirect('view_lab_request_detail_url', pk)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Lab_technician'])
def add_hematology_result(request, pk):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    staff = Staff.objects.get(basic_id=request.user.id)
    instance = {'hospital': hospital.id, 'staff': staff.id, 'patient': pk}
    if request.method == 'POST':
        hematology = HematologyResultForm(request.POST, instance=instance)
        staff = Staff.objects.get(basic_id=request.user.id)
        hospital = staff.hospital

        rqst = Hematology.objects.filter(hospital_id=hospital.id, requested_to_id=staff.id,
                                      patient_id=pk, status='pending').latest('date_of_request')
        waiting = HematologyWaitingList.objects.filter(hospital_id=hospital.id, requested_to_id=staff.id,
                                                    patient_id=pk, status='pending').latest('date_of_request')

        if hematology.is_valid():
            for s in hematology:
                setattr(rqst, s.name, hematology.cleaned_data.get(s.name))

            rqst.date_of_report = datetime.datetime.now()
            rqst.reported_by_id = staff.id
            rqst.status = 'reported'
            rqst.save()
            waiting.status = 'reported'
            waiting.save()
            return redirect('view_lab_request_detail_url', pk)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Lab_technician'])
def remove_from_list(request, pk):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    staff = Staff.objects.get(basic_id=request.user.id)

    rqst = StoolExamination.objects.get(hospital_id=hospital.id, requested_to_id=staff.id,
                                        patient_id=pk, status='pending')
    rqst.status = 'reported'
    staff.num_waiting = staff.num_waiting - 1
    rqst.save()
    staff.save()

    return redirect('lab_technician/lab_technician_homepage_url')

