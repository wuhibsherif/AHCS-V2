import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from accounts.models import Hospital, Staff
from login.decorators import allowed_users
from patient.models import UltraSound, XrayExamination, Patient
from radiologist.forms import XrayResultForm, UltraSoundResultForm

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Radiologist'])
def radiologist_homepage(request):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    request.session['healthcare_name'] = hospital.name
    staff = Staff.objects.get(basic_id=request.user.id)
    specialty = staff.specialty
    if specialty == 'Ultrasound':
        try:
            request_list = UltraSound.objects.filter(hospital_id=hospital.id, requested_to_id=staff.id,
                                                     status='pending')
            print(request_list)
            rqst_list = True
            context = {'hospital': hospital, 'rqst_list': rqst_list, 'request_list': request_list}
            return render(request, 'radiologist/homepage.html', context)
        except:
            rqst_list = False
            context = {'hospital': hospital, 'rqst_list': rqst_list}
            return render(request, 'radiologist/homepage.html', context)
        context = {'hospital': hospital}

    elif specialty == 'X-ray':
        try:
            request_list = XrayExamination.objects.filter(hospital_id=hospital.id, requested_to_id=staff.id,
                                                          status='pending')
            rqst_list = True
            context = {'hospital': hospital, 'rqst_list': rqst_list, 'request_list': request_list}
            return render(request, 'radiologist/homepage.html', context)
        except:
            rqst_list = False
            context = {'hospital': hospital, 'rqst_list': rqst_list}
            return render(request, 'radiologist/homepage.html', context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Radiology'])
def request_detail(request, pk):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    staff = Staff.objects.get(basic_id=request.user.id)
    request.session['healthcare_name'] = hospital.name
    user_profile = Patient.objects.get(id=pk)
    specialty = staff.specialty
    rqst = None
    result_form = None
    if specialty == 'Ultrasound':
        rqst = UltraSound.objects.get(hospital_id=hospital.id, requested_to_id=staff.id,
                                                     patient_id=pk, status='pending')
        if request.method == "POST":
            resultform = UltraSoundResultForm(request.POST, request.FILES)
            if resultform.is_valid():
                sonographic_report = resultform.cleaned_data.get("sonographic_report")
                img = resultform.cleaned_data.get("ultrasound_image")
                rqst.sonographic_report = sonographic_report
                rqst.ultra_sound_image = img
                rqst.date_of_report = datetime.datetime.now()
                rqst.save()
                result_form = UltraSoundResultForm
        else:
            result_form = UltraSoundResultForm

    elif specialty == 'X-ray':
        rqst = XrayExamination.objects.get(hospital_id=hospital.id, requested_to_id=staff.id,
                                              patient_id=pk, status='pending')
        if request.method == "POST":
            resultform = XrayResultForm(request.POST, request.FILES)
            if resultform.is_valid():
                impression = resultform.cleaned_data.get("impression")
                img = resultform.cleaned_data.get("x_ray_image")
                rqst.impressions = impression
                rqst.x_ray_image = img
                rqst.date_of_report = datetime.datetime.now()
                rqst.save()
                result_form = XrayResultForm
        else:
            result_form = XrayResultForm

    context = {'hospital': hospital, 'specialty': specialty, 'user_profile': user_profile,
               'rqst': rqst, 'result_form': result_form}
    return render(request, 'radiologist/request_detail.html', context)



@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Radiology'])
def remove_from_list(request, pk):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    staff = Staff.objects.get(basic_id=request.user.id)
    specialty = staff.specialty
    if specialty == 'Ultrasound':
        rqst = UltraSound.objects.get(hospital_id=hospital.id, requested_to_id=staff.id,
                                      patient_id=pk, status='pending')
        rqst.status = 'reported'
        staff.num_waiting = staff.num_waiting - 1
        rqst.save()
        staff.save()

    elif specialty == 'X-ray':
        rqst = XrayExamination.objects.get(hospital_id=hospital.id, requested_to_id=staff.id,
                                              patient_id=pk, status='pending')
        rqst.status = 'reported'
        staff.num_waiting = staff.num_waiting - 1
        rqst.save()
        staff.save()

    return redirect('radiologist/radiologist_homepage_url')