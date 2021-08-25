import datetime
from pyexpat import model
from time import timezone

from django import forms
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.models import Staff, User, Hospital
from lab_technician.models import UrineAnalysisWaitingList, HematologyWaitingList
from login import urls
from django.contrib.auth.decorators import login_required
from login import decorators
# Create your views here.

# @login_required(login_url='login_url')
# @decorators.physicianonly
from login.decorators import allowed_users
from patient.models import Patient, VitalSign, PatientForm, UltraSound, XrayExamination, StoolExamination, \
    UrineAnalysis, Hematology, Prescription, AdministeredTreatment
from physician.forms import AddPatientForm, ReferralRequestForm, PrescriptionForm, AdministeredTreatmentForm, \
    XrayRequestForm, UltrasoundRequestForm, UrineAnalysisRequestForm, StoolExaminationRequestForm, \
    HematologyExaminationRequestForm, AppointmentForm
from physician.models import PatientWaitingList, Referral, Appointment


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def physician_homepage(request):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    request.session['healthcare_name'] = hospital.name
    try:
        patient_waiting_list = PatientWaitingList.objects.filter(
            physician_id=Staff.objects.get(basic_id=request.user.id).id,
            status='pending')
        waiting_list = True
        context = {'patient_waiting_list': patient_waiting_list, 'waiting_list': waiting_list}
        return render(request, "physician/physician_dashboard.html", context)
    except:
        waiting_list = False
        context = {'waiting_list': waiting_list}
        return render(request, "physician/physician_dashboard.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def view_waiting_list(request):
    context = {}
    return render(request, "physician/forms/view_waiting_list.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def add_prescription(request):
    context = {}
    return render(request, "physician/forms/prescription_form.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def radiology_requests(request, pk):
    hospital_id = Staff.objects.get(basic_id=request.user.id).hospital.id
    xray_form = XrayRequestForm
    ultrasound_form = UltrasoundRequestForm
    context = {'xray_form': xray_form, 'ultrasound_form': ultrasound_form, 'pk': pk}
    return render(request, "physician/forms/xray_form.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def remove_from_list(request, pk):
    waiting_list = PatientWaitingList.objects.get(patient_id=pk, status='pending')
    waiting_list.status = 'approved'
    waiting_list.approval_time = datetime.datetime.now()
    waiting_list.save()
    staff = Staff.objects.get(basic_id=request.user.id)
    staff.num_waiting = staff.num_waiting - 1
    staff.save()
    return redirect('physician_homepage_url')


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def patient_detail(request, pk):
    user_profile = Patient.objects.get(id=pk)
    try:
        latest_patient_form = PatientForm.objects.filter(patient_id=pk).latest('date')
    except:
        latest_patient_form = None
    try:
        vital_sign = VitalSign.objects.filter(patient_id=pk).latest('taken_date')
    except:
        vital_sign = None
    try:
        referral = Referral.objects.get(patient_id=pk, status='pending')
        print(referral)
    except:
        print("no referral")
        referral = None
    patient_form = AddPatientForm
    prescription_form = PrescriptionForm
    hospital_id = Staff.objects.get(basic_id=request.user.id).hospital.id
    referral_request = ReferralRequestForm(pk=hospital_id)

    administered_treatment = AdministeredTreatmentForm
    context = {'patient': pk, 'user_profile': user_profile, 'vital_sign': vital_sign,
               'patient_form': patient_form, 'prescription_form': prescription_form, 'referral': referral,
               'latest_patient_form': latest_patient_form, 'administered_treatment': administered_treatment}
    return render(request, "physician/patient_detail.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def lab_request(request, pk):
    urine_analysis = UrineAnalysisRequestForm
    stool = StoolExaminationRequestForm
    hematology = HematologyExaminationRequestForm
    context = {'urine_analysis': urine_analysis, 'stool': stool, 'hematology': hematology, 'pk': pk}
    return render(request, "physician/forms/lab_request_form.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def add_patient_form(request, pk):
    if request.method == 'POST':
        patient_form = AddPatientForm(request.POST)
        patient = Patient.objects.get(id=pk)
        staff = Staff.objects.get(basic_id=request.user.id)
        hospital = staff.hospital
        context = {'patient': patient, 'staff': staff, 'hospital': hospital}
        if patient_form.is_valid():
            patient_form.save_patient_form(context)
            # nxt = request.POST.get('next', '/')
            return redirect('patient_detail_url', pk)
        else:
            patient_form = AddPatientForm(request.POST)
            patient = User.objects.get(id=pk)
            context = {'patient_form': patient_form, 'patient': patient}
            return render(request, "nurse/form/vital_sign_form.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def add_referral(request, pk):
    staff = Staff.objects.get(basic_id=request.user.id)
    hospital = staff.hospital
    patient = Patient.objects.get(id=pk)
    if request.method == 'POST':
        referral_form = ReferralRequestForm(request.POST)
        context = {'patient': patient, 'staff': staff, 'hospital': hospital}
        if referral_form.is_valid():
            referral_form.save_referral(context)
            # nxt = request.POST.get('next', '/')
            return redirect('patient_detail_url', pk)
        else:
            context = {'referral_form': referral_form, 'user_profile': patient}
            return render(request, "physician/forms/referral_request.html", context)
    referral_form = ReferralRequestForm(pk=hospital.id)
    context = {'referral_form': referral_form, 'user_profile': patient}
    return render(request, "physician/forms/referral_request.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def add_prescription(request, pk):
    patient = Patient.objects.get(id=pk)
    prescription_form = PrescriptionForm(request.POST or None)
    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)
        staff = Staff.objects.get(basic_id=request.user.id)
        hospital = staff.hospital
        context = {'patient': patient, 'staff': staff, 'hospital': hospital}
        if prescription_form.is_valid():
            prescription_form.save_prescription(context)
            # nxt = request.POST.get('next', '/')
            return redirect('patient_detail_url', pk)
        else:
            print(prescription_form.errors)
    context = {'prescription_form': prescription_form, 'user_profile': patient}
    return render(request, "physician/forms/patient_form.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def administered_treatment(request, pk):
    if request.method == 'POST':
        administered_treatment_form = AdministeredTreatmentForm(request.POST)
        patient = Patient.objects.get(id=pk)
        staff = Staff.objects.get(basic_id=request.user.id)
        hospital = staff.hospital
        context = {'patient': patient, 'staff': staff, 'hospital': hospital}
        if administered_treatment_form.is_valid():
            administered_treatment_form.save_administered_treatment(context)
            # nxt = request.POST.get('next', '/')
            return redirect('patient_detail_url', pk)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def add_xray_request(request, pk):
    if request.method == 'POST':
        xray_form = XrayRequestForm(request.POST)
        print(xray_form.is_valid())
        patient = Patient.objects.get(id=pk)
        staff = Staff.objects.get(basic_id=request.user.id)
        hospital = staff.hospital
        context = {'patient': patient, 'staff': staff, 'hospital': hospital}
        if xray_form.is_valid():
            xray_form.save_xray_request(context)
            # nxt = request.POST.get('next', '/')
            return redirect('radiology_request_url', pk)
        else:
            print(xray_form.errors)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def add_ultrasound_request(request, pk):
    ultrasound_request = UltrasoundRequestForm(request.POST)
    print(ultrasound_request.is_valid())
    patient = Patient.objects.get(id=pk)
    staff = Staff.objects.get(basic_id=request.user.id)
    hospital = staff.hospital
    context = {'patient': patient, 'staff': staff, 'hospital': hospital}
    if ultrasound_request.is_valid():
        ultrasound_request.save_ultrasound_request(context)
        # nxt = request.POST.get('next', '/')
        return redirect('radiology_request_url', pk)
    else:
        print(ultrasound_request.errors)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def view_lab_result_waiting_list(request):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    staff = Staff.objects.get(basic_id=request.user.id)
    reports = {}
    urine_report = UrineAnalysis.objects.filter(hospital_id=hospital.id, requested_by_id=staff.id, status='reported')
    if urine_report.all:
        reports['urine'] = urine_report
    hematology_report = Hematology.objects.filter(hospital_id=hospital.id, requested_by_id=staff.id, status='reported')
    if hematology_report.all:
        reports['hematology'] = hematology_report
    stool_report = StoolExamination.objects.filter(hospital_id=hospital.id, requested_by_id=staff.id, status='reported')
    if stool_report.all:
        reports['stool'] = stool_report
    context = {'hematology_report': hematology_report, 'urine_report': urine_report, 'stool_report': stool_report,
               'reports': reports}

    return render(request, "physician/forms/lab_result_waiting_list.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def view_radiology_result_waiting_list(request):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    staff = Staff.objects.get(basic_id=request.user.id)
    reports = {}
    ultra_report = UltraSound.objects.filter(hospital_id=hospital.id, requested_by_id=staff.id, status='reported')
    if ultra_report.all:
        reports['ultra'] = ultra_report
    xray_report = XrayExamination.objects.filter(hospital_id=hospital.id, requested_by_id=staff.id, status='reported')
    if xray_report.all:
        reports['xray'] = xray_report
    context = {'ultra_report': ultra_report, 'xray_report': xray_report, 'reports': reports}
    return render(request, "physician/forms/radiology_result_wating_list.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def patient_radiology_result_detail(request, pk):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    staff = Staff.objects.get(basic_id=request.user.id)
    ultra_report = UltraSound.objects.filter(hospital_id=hospital.id, requested_by_id=staff.id, status='reported',
                                             patient_id=pk)
    xray_report = XrayExamination.objects.filter(hospital_id=hospital.id, requested_by_id=staff.id, status='reported',
                                                 patient_id=pk)
    context = {'ultra_report': ultra_report, 'xray_report': xray_report, 'pk': pk}
    return render(request, "physician/forms/Patient_radiology_result.html", context)


def add_stool_examination_request(request, pk):
    if request.method == 'POST':
        stool = StoolExaminationRequestForm(request.POST)
        patient = Patient.objects.get(id=pk)
        staff = Staff.objects.get(basic_id=request.user.id)
        hospital = staff.hospital
        context = {'patient': patient, 'staff': staff, 'hospital': hospital}
        if stool.is_valid():
            lab_technician = Staff.objects.filter(hospital_id=context['hospital'].id, specialty='Lab_technician'). \
                order_by('-num_waiting').last()
            stool_request = StoolExamination.objects.create(
                patient_id=patient.id,
                requested_by_id=staff.id,
                requested_to_id=lab_technician.id,
                hospital_id=hospital.id,
            )
            for s in stool:
                if stool.cleaned_data.get(s.name):
                    setattr(stool_request, s.name, 'requested')
            stool_request.save()
            lab_tech = Staff.objects.get(id=lab_technician.id)
            lab_tech.num_waiting = staff.num_waiting + 1
            lab_tech.save()
            return redirect('lab_request_url', pk)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def add_urine_analysis_request(request, pk):
    if request.method == 'POST':
        urine_analysis = UrineAnalysisRequestForm(request.POST)
        patient = Patient.objects.get(id=pk)
        staff = Staff.objects.get(basic_id=request.user.id)
        hospital = staff.hospital
        context = {'patient': patient, 'staff': staff, 'hospital': hospital}
        if urine_analysis.is_valid():
            lab_technician = Staff.objects.filter(hospital_id=context['hospital'].id, specialty='Lab_technician'). \
                order_by('-num_waiting').last()
            urine_analysis_object = UrineAnalysis.objects.create(
                patient_id=patient.id,
                requested_by_id=staff.id,
                requested_to_id=lab_technician.id,
                hospital_id=hospital.id,
            )
            urine_rqst = UrineAnalysisWaitingList.objects.create(
                patient_id=patient.id,
                requested_by_id=staff.id,
                requested_to_id=lab_technician.id,
                hospital_id=hospital.id,
            )
            for urine in urine_analysis:
                if urine_analysis.cleaned_data.get(urine.name):
                    setattr(urine_rqst, urine.name, True)
            urine_analysis_object.save()
            urine_rqst.save()
            lab_tech = Staff.objects.get(id=lab_technician.id)
            lab_tech.num_waiting = staff.num_waiting + 1
            lab_tech.save()
            return redirect('lab_request_url', pk)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def add_hematology_request(request, pk):
    if request.method == 'POST':
        hematology_request = HematologyExaminationRequestForm(request.POST)
        patient = Patient.objects.get(id=pk)
        staff = Staff.objects.get(basic_id=request.user.id)
        hospital = staff.hospital
        context = {'patient': patient, 'staff': staff, 'hospital': hospital}
        if hematology_request.is_valid():
            lab_technician = Staff.objects.filter(hospital_id=context['hospital'].id, specialty='Lab_technician'). \
                order_by('-num_waiting').last()
            hematology_object = Hematology.objects.create(
                patient_id=patient.id,
                requested_by_id=staff.id,
                requested_to_id=lab_technician.id,
                hospital_id=hospital.id,
            )
            hematology_rqst = HematologyWaitingList.objects.create(
                patient_id=patient.id,
                requested_by_id=staff.id,
                requested_to_id=lab_technician.id,
                hospital_id=hospital.id,
            )
            for hematology in hematology_request:
                if hematology_request.cleaned_data.get(hematology.name):
                    setattr(hematology_rqst, hematology.name, True)
            hematology_object.save()
            hematology_rqst.save()
            lab_tech = Staff.objects.get(id=lab_technician.id)
            lab_tech.num_waiting = staff.num_waiting + 1
            lab_tech.save()
            return redirect('lab_request_url', pk)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def lab_result_detail(request, pk):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    staff = Staff.objects.get(basic_id=request.user.id)
    urine_report = UrineAnalysis.objects.filter(hospital_id=hospital.id, requested_by_id=staff.id, status='reported',
                                                patient_id=pk)
    stool_report = StoolExamination.objects.filter(hospital_id=hospital.id, requested_by_id=staff.id, status='reported',
                                                   patient_id=pk)

    hematology_report = Hematology.objects.filter(hospital_id=hospital.id, requested_by_id=staff.id, status='reported',
                                                  patient_id=pk)
    context = {'urine_report': urine_report, 'stool_report': stool_report, 'hematology_report': hematology_report,
               'pk': pk}
    return render(request, "physician/forms/lab_result_detail.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def medical_history(request, pk):
    all_patient_form = PatientForm.objects.filter(patient_id=pk).order_by('-date')
    all_patient_form_paginator = Paginator(all_patient_form, 2)
    page = request.GET.get('page')
    form_paginate = all_patient_form_paginator.get_page(page)

    all_vital_sign = VitalSign.objects.filter(patient_id=pk).order_by('-taken_date')
    vital_sign_paginator = Paginator(all_vital_sign, 5)
    vital_page = request.GET.get('page')
    vital_sign_paginate = vital_sign_paginator.get_page(vital_page)

    all_prescriptions = Prescription.objects.filter(patient_id=pk, status='taken').order_by('-prescription_date')
    administered_treatment = AdministeredTreatment.objects.filter(patient_id=pk).order_by('-medication_date')

    context = {'all_patient_form': form_paginate, 'all_vital_sign': vital_sign_paginate,
               'all_prescriptions': all_prescriptions, 'all_administered_treatment': administered_treatment}
    print(all_vital_sign)
    return render(request, "physician/forms/medical_history.html", context)


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['Physician'])
def add_appointment(request, pk):
    patient = Patient.objects.get(id=pk)
    appointment_form = AppointmentForm(request.POST or None)
    if request.method == 'POST':
        staff = Staff.objects.get(basic_id=request.user.id)
        hospital = staff.hospital
        context = {'patient': patient, 'staff': staff, 'hospital': hospital}
        if appointment_form.is_valid():
            appointment_form.save_appointment(context)
            messages.success(request, "Appointement Added Successfully")
            return redirect('patient_detail_url', pk)
        else:
            print(appointment_form.errors)
    context = {'appointment_form': appointment_form, 'user_profile': patient}
    return render(request, "physician/forms/add_appointment.html", context)


def checkdisease(request):
    diseaselist = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer diseae',
                   'AIDS', 'Diabetes ',
                   'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine', 'Cervical spondylosis',
                   'Paralysis (brain hemorrhage)',
                   'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B',
                   'Hepatitis C', 'Hepatitis D',
                   'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia',
                   'Dimorphic hemmorhoids(piles)',
                   'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
                   'Osteoarthristis',
                   'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinary tract infection',
                   'Psoriasis', 'Impetigo']

    symptomslist = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills',
                    'joint_pain',
                    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
                    'spotting_ urination',
                    'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss',
                    'restlessness', 'lethargy',
                    'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes',
                    'breathlessness', 'sweating',
                    'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea',
                    'loss_of_appetite', 'pain_behind_the_eyes',
                    'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
                    'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
                    'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
                    'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
                    'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
                    'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
                    'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
                    'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
                    'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
                    'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
                    'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
                    'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
                    'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body',
                    'belly_pain',
                    'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite',
                    'polyuria', 'family_history', 'mucoid_sputum',
                    'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
                    'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
                    'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf',
                    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
                    'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
                    'red_sore_around_nose',
                    'yellow_crust_ooze']

    alphabaticsymptomslist = sorted(symptomslist)

    if request.method == 'GET':

        return render(request, 'patient/checkdisease/checkdisease.html', {"list2": alphabaticsymptomslist})




    elif request.method == 'POST':

        ## access you data by playing around with the request.POST object

        inputno = int(request.POST["noofsym"])
        print(inputno)
        if (inputno == 0):
            return JsonResponse({'predicteddisease': "none", 'confidencescore': 0})

        else:

            psymptoms = []
            psymptoms = request.POST.getlist("symptoms[]")

            print(psymptoms)

            """      #main code start from here...
            """

            testingsymptoms = []
            # append zero in all coloumn fields...
            for x in range(0, len(symptomslist)):
                testingsymptoms.append(0)

            # update 1 where symptoms gets matched...
            for k in range(0, len(symptomslist)):

                for z in psymptoms:
                    if (z == symptomslist[k]):
                        testingsymptoms[k] = 1

            inputtest = [testingsymptoms]

            print(inputtest)

            predicted = model.predict(inputtest)
            print("predicted disease is : ")
            print(predicted)

            y_pred_2 = model.predict_proba(inputtest)
            confidencescore = y_pred_2.max() * 100
            print(" confidence score of : = {0} ".format(confidencescore))

            confidencescore = format(confidencescore, '.0f')
            predicted_disease = predicted[0]

            # consult_doctor codes----------

            #   doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
            #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]

            Rheumatologist = ['Osteoarthristis', 'Arthritis']

            Cardiologist = ['Heart attack', 'Bronchial Asthma', 'Hypertension ']

            ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo', 'Hypothyroidism']

            Orthopedist = []

            Neurologist = ['Varicose veins', 'Paralysis (brain hemorrhage)', 'Migraine', 'Cervical spondylosis']

            Allergist_Immunologist = ['Allergy', 'Pneumonia',
                                      'AIDS', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue', 'Typhoid']

            Urologist = ['Urinary tract infection',
                         'Dimorphic hemmorhoids(piles)']

            Dermatologist = ['Acne', 'Chicken pox', 'Fungal infection', 'Psoriasis', 'Impetigo']

            Gastroenterologist = ['Peptic ulcer diseae', 'GERD', 'Chronic cholestasis', 'Drug Reaction',
                                  'Gastroenteritis', 'Hepatitis E',
                                  'Alcoholic hepatitis', 'Jaundice', 'hepatitis A',
                                  'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Diabetes ', 'Hypoglycemia']

            if predicted_disease in Rheumatologist:
                consultdoctor = "Rheumatologist"

            if predicted_disease in Cardiologist:
                consultdoctor = "Cardiologist"


            elif predicted_disease in ENT_specialist:
                consultdoctor = "ENT specialist"

            elif predicted_disease in Orthopedist:
                consultdoctor = "Orthopedist"

            elif predicted_disease in Neurologist:
                consultdoctor = "Neurologist"

            elif predicted_disease in Allergist_Immunologist:
                consultdoctor = "Allergist/Immunologist"

            elif predicted_disease in Urologist:
                consultdoctor = "Urologist"

            elif predicted_disease in Dermatologist:
                consultdoctor = "Dermatologist"

            elif predicted_disease in Gastroenterologist:
                consultdoctor = "Gastroenterologist"

            else:
                consultdoctor = "other"



            # saving to database.....................

            diseasename = predicted_disease
            no_of_symp = inputno
            symptomsname = psymptoms
            confidence = confidencescore



            print("disease record saved sucessfully.............................")
            context = {{'predicteddisease': predicted_disease, 'confidencescore': confidencescore,
                                 "consultdoctor": consultdoctor}}
            return render(request, "physician/forms/add_appointment.html", context)


def view_sugggestion(request):
    return render(request, "physician/forms/view_suggestion.html")


def view_appointment(request):
    appointment = Appointment.objects.filter(physician_id=Staff.objects.get(basic_id=request.user.id).id, status='pending')
    return render(request, "physician/forms/view_appointment.html", {'appointment': appointment})