import datetime

from django import forms
import django.forms.widgets

from patient.models import Prescription


class DateInput(forms.DateInput):
    input_type = 'date'


class Medication_Form(forms.Form):
    name = forms.CharField(required=True, max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    frequency = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'type': 'date'}))
    start_date = forms.DateField(required=True, widget=DateInput)
    end_date = forms.DateField(required=True, widget=DateInput)

    def save_medication_detail(self, context):
        medication = Prescription.objects.get(id=context['prescription'].id)
        print(medication)
        medication.medication_name = self.cleaned_data.get('name')
        medication.pharmacy_id = context['pharmacy'].id
        medication.frequency_perday = self.cleaned_data.get('frequency')
        medication.description = self.cleaned_data.get('description')
        medication.start_date = self.cleaned_data.get('start_date')
        medication.end_date = self.cleaned_data.get('end_date')
        medication.bought_on_date = datetime.datetime.now()
        medication.status = 'taken'
        medication.save()


class PatientAuthenticationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username here...'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password here...'}))
