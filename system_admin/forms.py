from django import forms
from accounts.models import *


class HealthCareProviderRegistrationForm(forms.Form):
    type_choice = (
        ('Hospital', 'Hospital'), ('Pharmacy', 'Pharmacy')
    )
    region_choice = (
        ("Tigray", "Tigray"), ("Afar", "Afar"), ("Amhara", "Amhara"), ("Oromia", "Oromia"), ("Somali", "Somali"),
        ("Benishangul-Gumuz", "Benishangul-Gumuz"), ("Gambela", "Gambela"), ("Harari", "Harari"), ("Sidama", "Sidama"),
        (
            "Southern Nations, Nationalities, and Peoples' Region",
            "Southern Nations, Nationalities, and Peoples' Region"),
        ("Addis Ababa", "Addis Ababa"), ("Dire Dawa", "Dire Dawa")
    )
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name here... '}))
    region = forms.CharField(required=True,
                             widget=forms.Select(choices=region_choice,
                                                 attrs={'class': 'form-control', 'placeholder': 'Region here.. '}))
    zone = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zone here... '}))
    woreda = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Woreda here... '}))
    kebele = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kebele here... '}))
    phone = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Phone number here..'}))
    type = forms.CharField(required=True, max_length=50, widget=forms.Select(choices=type_choice,
                                                                             attrs={'class': 'form-control',
                                                                                    'placeholder': 'healthcare type '
                                                                                                   'here... '}))

    def save_healthcare_provider(self, admin_id):
        if self.cleaned_data.get('type') == 'Hospital':
            new_hospital_address = Address.objects.create(
                region=self.cleaned_data.get('region'),
                zone=self.cleaned_data.get('zone'),
                woreda=self.cleaned_data.get('woreda'),
                kebele=self.cleaned_data.get('kebele'),

            )

            new_hospital = Hospital.objects.create(
                address_id=new_hospital_address.id,
                admin_id=admin_id,
                name=self.cleaned_data.get('name'),
                phone=self.cleaned_data.get('phone'),
            )
            new_hospital_address.save()
            new_hospital.save()
        else:
            new_pharmacy_address = Address.objects.create(
                region=self.cleaned_data.get('region'),
                zone=self.cleaned_data.get('zone'),
                woreda=self.cleaned_data.get('woreda'),
                kebele=self.cleaned_data.get('kebele'),

            )
            new_pharmacy = Pharmacy.objects.create(
                address_id=new_pharmacy_address.id,
                name=self.cleaned_data.get('name'),
                admin_id=admin_id,
                phone=self.cleaned_data.get('phone'),
            )
            new_pharmacy_address.save()
            new_pharmacy.save()
