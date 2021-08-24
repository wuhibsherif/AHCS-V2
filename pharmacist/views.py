from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from accounts.models import Pharmacy, Staff
from login.decorators import allowed_users
from patient.models import Patient, Prescription
from pharmacist.forms import Medication_Form, PatientAuthenticationForm
from pharmacist.models import Pharmacist


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['pharmacist'])
def pharmacist_homepage(request):
    pharmacy = Pharmacist.objects.get(basic_id=request.user.id).pharmacy
    request.session['healthcare_name'] = pharmacy.name
    return render(request, 'pharmacist/homepage.html')


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['pharmacist'])
def add_medication_details(request, pk, pk2):
    patient = Patient.objects.get(id=pk)
    medication = Medication_Form(request.POST or None)
    if request.method == 'POST':
        patient = Patient.objects.get(id=pk)
        pharmacist = Pharmacist.objects.get(basic_id=request.user.id)
        pharmacy = Pharmacy.objects.get(id=pharmacist.pharmacy_id)
        prescription = Prescription.objects.get(id=pk2)
        print(prescription.id)
        context = {'patient': patient, 'pharmacy': pharmacy, 'prescription': prescription}
        if medication.is_valid():
            print("valid")
            medication.save_medication_detail(context)
            # nxt = request.POST.get('next', '/')
            return redirect('prescription_detail_url', patient.basic_id)
        else:
            print(medication.errors)

    context = {'medication': medication, 'user_profile': patient}
    return render(request, 'pharmacist/pharmacist_add_medication_detail.html', context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['pharmacist'])
def authenticate_patient(request):
    msg = None
    form = PatientAuthenticationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(password)
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None and user.role == 'patient':
                print(username)
                return redirect('prescription_detail_url', user.id)
            else:
                msg = 'Username Or Password Incorrect'
                context = {'form': form, 'msg': msg, 'found': True}
                return render(request, 'profiles/pharmacist_patient_found.html', context)
        else:
            msg = form.errors
    context = {'form': form, 'msg': msg}
    return render(request, 'profiles/pharmacist_patient_found.html', context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['pharmacist'])
def prescription_detail(request, pk):
    patient = Patient.objects.get(basic_id=pk)
    prescription = Prescription.objects.filter(patient_id=patient.id, status='pending')
    print(prescription)
    context = {'user_profile': patient, 'found': True,
               'prescription': prescription}
    return render(request, 'profiles/pharmacist_patient_profile.html', context)
