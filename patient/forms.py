import datetime

from django import forms

from patient.models import VitalSign
from receptionist.models import Triage


class VitalSignForm(forms.Form):
    weight = forms.IntegerField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'weight here... '}))
    height = forms.IntegerField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'height here... '}))
    systolic_BP = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ' '}))
    diastolic_BP = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''}))
    temperature = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ' '}))
    respiratory_rate = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'h '}))
    heart_rate = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ' '}))
    urine_output = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''}))
    blood_sugar_F = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''}))
    blood_sugar_R = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''}))
    comment = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''}))

    def save_vital_sign(self, context):
        h = self.cleaned_data.get('height')
        w = self.cleaned_data.get('weight')
        print('saving vital sign...')
        print(h)
        print(w)
        bmi = w / pow(h / 100, 2)
        print(bmi)
        vital_sign = VitalSign.objects.create(
            patient_id=context['patient'].id,
            weight=self.cleaned_data.get('weight'),
            height=self.cleaned_data.get('height'),
            bmi=bmi,
            temperature=self.cleaned_data.get('temperature'),
            systolic_BP=self.cleaned_data.get('systolic_BP'),
            diastolic_BP=self.cleaned_data.get('diastolic_BP'),

            respiratory_rate=self.cleaned_data.get('respiratory_rate'),
            heart_rate=self.cleaned_data.get('heart_rate'),
            urine_output=self.cleaned_data.get('urine_output'),
            blood_sugar_R=self.cleaned_data.get('blood_sugar_R'),
            blood_sugar_F=self.cleaned_data.get('blood_sugar_F'),
            taken_by_id=context['staff'].id,
            comment=self.cleaned_data.get('comment'),

            taken_date=datetime.datetime.now(),
            taken_at_hospital_id=context['hospital'].id

        )
        vital_sign.save()
        return vital_sign.patient_id
