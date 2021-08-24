from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from accounts.models import Hospital, Staff
from admission_and_discharge.forms import DepartmentSelectionForm
from login import decorators
from physician.models import Referral


@login_required(login_url='login_url')
@decorators.allowed_users(allowed_roles=['Admission and discharge'])
def admission_and_discharge_homepage(request):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    request.session['healthcare_name'] = hospital.name
    return render(request, "admission_and_discharge/homepage.html")


@login_required(login_url='login_url')
@decorators.allowed_users(allowed_roles=['Admission and discharge'])
def referral_from_other_healthcare(request):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    referrals = Referral.objects.filter(referred_to_hospital_id=hospital.id)
    context = {'referrals': referrals}
    print(referrals)
    return render(request, "admission_and_discharge/referral_from_others.html", context)


def referral_to_other_healthcare(request):
    return None


def referral_from_internal(request):
    return None


def referral_detail(request, pk):
    if request.method == 'POST':
        referral = Referral.objects.get(id=pk)
        form = DepartmentSelectionForm(request.POST)
        department = form.cleaned_data.get('department')
        print(department)
        return render(request, "admission_and_discharge/view_referral_detail.html")
    choices = [(staff['specialty'], staff['specialty']) for staff in Staff.objects.filter(hospital_id=Staff.objects.get(basic_id=request.user.id).hospital_id).values('specialty').exclude(specialty=None).exclude(specialty='Lab_technician').exclude(specialty='X-ray').exclude(specialty='Ultrasound').exclude(specialty='Lab_technician').distinct()]
    print(choices[0])
    referral = Referral.objects.get(id=pk)
    hospital_id = Staff.objects.get(basic_id=request.user.id).hospital_id
    department = DepartmentSelectionForm(pk=choices)
    context = {'referral': referral, 'department': department}
    return render(request, "admission_and_discharge/view_referral_detail.html", context)
