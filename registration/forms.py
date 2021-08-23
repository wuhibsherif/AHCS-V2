from django import forms

from hospital_admin.forms import UserRegistrationForm
from login.models import User

from login.models import User
from system_admin.models import HealthCareProvider


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

    def save_hospital(self):
        password = User.objects.make_random_password()
        count = User.objects.count()

        new_hospital = Hospital.objects.create(
            name=self.cleaned_data.get('name'),
            region=self.cleaned_data.get('region'),
            zone=self.cleaned_data.get('zone'),
            woreda=self.cleaned_data.get('woreda'),
            kebele=self.cleaned_data.get('kebele'),
            phone=self.cleaned_data.get('phone'),
            type=self.cleaned_data.get('type'),

        )
        new_hospital.save_hospital()

        def save_pharmacy(self):
            password = User.objects.make_random_password()
            count = User.objects.count()

            new_pharmacy = Pharmacy.objects.create(
                name=self.cleaned_data.get('name'),
                region=self.cleaned_data.get('region'),
                zone=self.cleaned_data.get('zone'),
                woreda=self.cleaned_data.get('woreda'),
                kebele=self.cleaned_data.get('kebele'),
                phone=self.cleaned_data.get('phone'),
                type=self.cleaned_data.get('type'),

            )
            new_pharmacy = Pharmacy.save_pharmacy()
