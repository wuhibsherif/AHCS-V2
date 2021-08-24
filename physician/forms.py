import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.http import request
from django.utils.datetime_safe import date

from accounts.models import Hospital, User, Staff
from patient.models import PatientForm, Prescription, AdministeredTreatment, XrayExamination, UltraSound
from physician.models import Referral, Appointment


class AddPatientForm(forms.Form):
    note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)

    def save_patient_form(self, context):
        patient_form = PatientForm.objects.create(
            hospital_id=context['hospital'].id,
            patient_id=context['patient'].id,
            note=self.cleaned_data.get('note'),
            filled_by_id=context['staff'].id,
            date=datetime.datetime.now()
        )
        patient_form.save()


class DateInput(forms.DateInput):
    input_type = 'date'


def no_past(value):
    today = date.today()
    if value < today:
        raise ValidationError('Appointment Date cannot be in the past.')


class AppointmentForm(forms.Form):
    case = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form-control"}))
    appointment_date = forms.DateField(required=True, widget=DateInput, validators=[no_past])

    def clean_appointment_date(self, *args, **kwargs):
        value = self.cleaned_data.get('appointment_date')
        today = date.today()
        if value < today:
            raise ValidationError('Appointment_Date cannot be in the past.')
        return value

    def save_appointment(self, context):
        new_appointment = Appointment.objects.create(
            physician_id=context['staff'].id,
            hospital_id=context['hospital'].id,
            patient_id=context['patient'].id,
            appointment_date=self.cleaned_data.get('appointment_date'),
            booked_date=datetime.datetime.now(),
            case=self.cleaned_data.get('case'),
            status="pending")
        new_appointment.save()


class ReferralRequestForm(forms.Form):
    health_problem_identified_in_detail = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),
                                                          required=True)
    identified_disease_type = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'disease type here... '}))
    action_taken = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'action taken here... '}))
    reason_for_referral = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'reason for referral here... '}))
    referred_to_hospital = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    '''def set_hospital_choice(self, pk):
        self.fields['referred_to_hospital'].choices = [(hospital.id, hospital.name) for hospital in Hospital
            .objects.all().exclude(id=pk)]'''

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)  # store value of request
        super(ReferralRequestForm, self).__init__(*args, **kwargs)
        print(self.pk)
        self.fields['referred_to_hospital'].choices = [(hospital.id, hospital.name) for hospital in Hospital
            .objects.all().exclude(id=self.pk)]

    def save_referral(self, context):
        referral = Referral.objects.create(
            referred_by_id=context['staff'].id,
            referring_hospital_id=context['hospital'].id,
            referred_to_hospital_id=self.cleaned_data.get('referred_to_hospital'),
            patient_id=context['patient'].id,
            health_problem_identified_in_detail=self.cleaned_data.get('health_problem_identified_in_detail'),
            action_taken=self.cleaned_data.get('action_taken'),
            reason_for_referral=self.cleaned_data.get('reason_for_referral'),
            referral_date=datetime.datetime.now(),
        )
        referral.save()


class XrayRequestForm(forms.Form):
    examination_requested = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    finding_and_diagnosis = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))

    '''def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)  # store value of request
        super(XrayRequestForm, self).__init__(*args, **kwargs)
        print(self.pk)
        self.fields['requested_to'].choices = [(radiologist.id, radiologist.basic.username) for radiologist in
                                               Staff.objects.filter(hospital_id=self.pk, specialty='X-ray')]'''

    def save_xray_request(self, context):
        radiologist = Staff.objects.filter(hospital_id=context['hospital'].id, specialty='X-ray'). \
            order_by('-num_waiting').last().id
        xray_request = XrayExamination.objects.create(
            hospital_id=context['hospital'].id,
            patient_id=context['patient'].id,
            requested_by_id=context['staff'].id,
            requested_to_id=radiologist,
            examination_requested=self.cleaned_data.get('examination_requested'),
            finding_and_diagnosis=self.cleaned_data.get('finding_and_diagnosis'),
        )
        xray_request.save()
        staff = Staff.objects.get(id=radiologist)
        staff.num_waiting = staff.num_waiting + 1
        staff.save()


class UltrasoundRequestForm(forms.Form):
    organ_to_be_examined = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    '''def set_requested_to_choice(self, pk):
        self.fields['requested_to'].choices = [(radiologist.id, radiologist.basic.username) for
                                               radiologist in
                                               Staff.objects.filter(hospital_id=Staff.objects.get(basic_id=pk).
                                                                    hospital_id, specialty='ultrasound')]'''

    def save_ultrasound_request(self, context):
        radiologist = Staff.objects.filter(hospital_id=context['hospital'].id, specialty='Ultrasound'). \
            order_by('-num_waiting').last()
        ultrasound_request = UltraSound.objects.create(
            hospital_id=context['hospital'].id,
            patient_id=context['patient'].id,
            requested_by_id=context['staff'].id,
            requested_to_id=radiologist.id,
            organ_to_be_examined=self.cleaned_data.get('organ_to_be_examined'),
        )
        ultrasound_request.save()
        staff = Staff.objects.get(id=radiologist)
        staff.num_waiting = staff.num_waiting + 1
        staff.save()


class AdministeredTreatmentForm(forms.Form):
    medication_name = forms.CharField(required=True, max_length=150,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def save_administered_treatment(self, context):
        administered_treatment = AdministeredTreatment.objects.create(
            hospital_id=context['hospital'].id,
            patient_id=context['patient'].id,
            given_by_id=context['staff'].id,
            medication_name=self.cleaned_data.get('medication_name'),
            description=self.cleaned_data.get('description'),
            medication_date=datetime.datetime.now(),
        )
        administered_treatment.save()


class PrescriptionForm(forms.Form):
    prescription_detail = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def save_prescription(self, context):
        prescription = Prescription.objects.create(
            hospital_id=context['hospital'].id,
            patient_id=context['patient'].id,
            prescription_detail=self.cleaned_data.get('prescription_detail'),
            prescribed_by_id=context['staff'].id,
            prescription_date=datetime.datetime.now()
        )
        prescription.save()


class UrineAnalysisRequestForm(forms.Form):
    albumine = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    blood = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    chemo_leukocyte = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    glucose = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    PH = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    nitrate = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    urobilonogen = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    ketone = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    bilirubin = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    specific_gravity = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    microscopy_leukocyte = forms.BooleanField(required=False,
                                              widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    erythrocyte = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    yeast = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    bacteria = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    squamous_epithelial_cell = forms.BooleanField(required=False,
                                                  widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    hyaline_cast = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    granular_cast = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    WBC_casts = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    RBC_cast = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    uric_acid = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    calcium_oxalate = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    triple_phosphate = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))


class StoolExaminationRequestForm(forms.Form):
    parasites = forms.BooleanField(required=False,
                                   widget=forms.CheckboxInput(attrs={'class': 'form-control' 'checkbox'}))
    pus_cell = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    red_blood_cell = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    yeast_cell = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    occult_blood_test = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    h_pylory_stool_ag_test = forms.BooleanField(required=False,
                                                widget=forms.CheckboxInput(attrs={'class': 'form-control'}))


class HematologyExaminationRequestForm(forms.Form):
    CBC = forms.BooleanField(required=False,
                             widget=forms.CheckboxInput(attrs={'class': 'form-control' 'fancy-checkbox'}))
    BE = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    TWBC = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    differential = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    neutrophil = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    lymphocyte = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    eocynophil = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    basophiles = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    monocyt = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    haemoglobin = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    hemo_TCRIT = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    MCV = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    MCH = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    MCHC = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    RBC = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    RBC_morphology = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    platlet_count = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    EST = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    bleeding_time_test = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    clot_retraction = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    coagulation_time = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    prothrombin_time = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    PTT = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    FBS_RBS = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    blood_group = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    fibrinogen = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    coombs_test = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    CD4 = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
