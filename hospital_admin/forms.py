import re
import unicodedata
import phonenumbers

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from past.builtins import unicode

from accounts.models import *
from patient.models import Patient
from pharmacist.models import Pharmacist


class user_form(UserCreationForm):
    class Meta:
        model = User
        fields = ('role',)


def generate_username(full_name):
    name = full_name.split(' ')
    lastname = name[-1]
    middlename = name[1]
    firstname = name[0]
    print(firstname)
    print(lastname)

    # try first name initials plus last full name
    username = '%s%s' % (firstname[0], lastname)
    if User.objects.filter(username=username).count() > 0:
        # if that doesn't fit, try full first name plus last name initials
        username = '%s%s' % (firstname, lastname[0])
        if User.objects.filter(username=username).count() > 0:
            # if that doesn't fit, try first name initials plus full middlne name
            username = '%s%s' % (firstname[0], middlename)
            if User.objects.filter(username=username).count() > 0:
                # if it doesn't fit, put the first name plus a number
                users = User.objects.filter(username__regex=r'^%s[1-9]{1,}$' % firstname).order_by('username').values(
                    'username')
                if len(users) > 0:
                    last_number_used = sorted(map(lambda x: int(x['username'].replace(firstname, '')), users))
                    last_number_used = last_number_used[-1]
                    number = last_number_used + 1
                    username = '%s%s' % (firstname, number)
                else:
                    username = '%s%s' % (firstname, 1)
    return username


class UserRegistrationForm(forms.Form):
    speciality_choice = [('Internal medicine', 'Internal medicine'), ('Pediatrics', 'Pediatrics'),
                         ('Dermatology', 'Dermatology'),
                         ('Ophthalmology', 'Ophthalmology'), ('Oncology', 'Oncology'), ('Obstetrics', 'Obstetrics')
                         ]
    radiology_speciality_choice = [('X-ray', 'X-ray'), ('Ultrasound', 'Ultrasound')]
    role_choices = [('Receptionist', 'Receptionist'), ('Physician', speciality_choice), ('Nurse', 'Nurse'),
                    ('Radiologist', radiology_speciality_choice), ('Lab_technician', 'Lab_technician'),
                    ('Pharmacist', 'Pharmacist')]
    sex_choices = [('Male', 'Male'), ('Female', 'Female')]
    region_choice = (
        ("Tigray", "Tigray"), ("Afar", "Afar"), ("Amhara", "Amhara"), ("Oromia", "Oromia"), ("Somali", "Somali"),
        ("Benishangul-Gumuz", "Benishangul-Gumuz"), ("Gambela", "Gambela"), ("Harari", "Harari"), ("Sidama", "Sidama"),
        (
            "Southern Nations, Nationalities, and Peoples' Region",
            "Southern Nations, Nationalities, and Peoples' Region"),
        ("Addis Ababa", "Addis Ababa"), ("Dire Dawa", "Dire Dawa")
    )
    firstname = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name here... '}))
    middlename = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Middle Name here... '}))
    lastname = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name here... '}))
    sex = forms.CharField(required=True, max_length=10,
                          widget=forms.Select(choices=sex_choices,
                                              attrs={'class': 'form-control', 'placeholder': 'Sex here... '}))
    age = forms.IntegerField(required=True,
                             widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age here... '}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email here... '}))
    region = forms.CharField(required=True,
                             widget=forms.Select(choices=region_choice,
                                                 attrs={'class': 'form-control', 'placeholder': 'Region here.. '}))
    zone = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zone here... '}))
    woreda = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Woreda here... '}))
    kebele = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kebele here... '}))
    house_no = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'House No here...'}))
    phone = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Phone number here..'}))
    role = forms.CharField(required=False, max_length=50, widget=forms.Select(choices=role_choices,
                                                                              attrs={'class': 'form-control',
                                                                                     'placeholder': 'Role here... '}))

    def clean_firstname(self, *args, **kwargs):
        firstname = self.cleaned_data.get('firstname')
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if any(chr.isdigit() for chr in firstname):
            raise forms.ValidationError("name can not contain number or character")
        if (regex.search(firstname) != None):
            raise forms.ValidationError("name can not contain number or character")
        else:
            return str(firstname)

    def clean_middlename(self, *args, **kwargs):
        middlename = self.cleaned_data.get('middlename')
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if any(chr.isdigit() for chr in middlename):
            raise forms.ValidationError("name can not contain number or character")
        if (regex.search(middlename) != None):
            raise forms.ValidationError("name can not contain number or character")
        else:
            return str(middlename)

    def clean_lastname(self, *args, **kwargs):
        lastname = self.cleaned_data.get('lastname')
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if any(chr.isdigit() for chr in lastname):
            raise forms.ValidationError("name can not contain number or character")
        if (regex.search(lastname) != None):
            raise forms.ValidationError("name can not contain number or character")
        else:
            return str(lastname)

    ''' def clean_phone(self, *args, **kwargs):
        phone = self.cleaned_data.get('phone')
        z = phonenumbers.parse(phone, "ET")
        if not phonenumbers.is_valid_number(z):
            raise forms.ValidationError("In valid format")
        return phone
    '''
    def clean_age(self, *args, **kwargs):
        age = self.cleaned_data.get('age')
        if age < 1 or age > 200:
            raise forms.ValidationError("age can not be 0 or greater than 150")
        return age

    def clean_zone(self, *args, **kwargs):
        zone = self.cleaned_data.get('zone')
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if (regex.search(zone) != None):
            raise forms.ValidationError("This is not a valid zone name")
        if any(chr.isdigit() for chr in zone):
            raise forms.ValidationError("This is not a valid zone name")

        return zone

    def clean_woreda(self, *args, **kwargs):
        woreda = self.cleaned_data.get('woreda')
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if (regex.search(woreda) != None):
            raise forms.ValidationError("This is not valid name")

        return woreda

    def clean_kebele(self, *args, **kwargs):
        kebele = self.cleaned_data.get('kebele')
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if (regex.search(kebele) != None):
            raise forms.ValidationError("This is not valid name")
        return kebele

    def clean_house_no(self, *args, **kwargs):
        house_no = self.cleaned_data.get('house_no')
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if (regex.search(house_no) != None):
            raise forms.ValidationError("This is not valid name")
        return house_no

    def save_patient(self, context):
        password = User.objects.make_random_password()
        new_patient_address = Address.objects.create(
            region=self.cleaned_data.get('region'),
            zone=self.cleaned_data.get('zone'),
            woreda=self.cleaned_data.get('woreda'),
            kebele=self.cleaned_data.get('kebele'),
            house_no=self.cleaned_data.get('house_no'),
        )
        full_name = self.cleaned_data.get('firstname') + ' ' + self.cleaned_data.get(
            'lastname') + ' ' + self.cleaned_data.get('middlename')
        username = (generate_username(full_name))

        new_patient_info = User.objects.create(
            first_name=self.cleaned_data.get('firstname'),
            last_name=self.cleaned_data.get('lastname'),
            middle_name=self.cleaned_data.get('middlename'),
            email=self.cleaned_data.get('email'),
            sex=self.cleaned_data.get('sex'),
            age=self.cleaned_data.get('age'),
            address_id=new_patient_address.id,
            phone=self.cleaned_data.get('phone'),
            username=username,
            role="patient",

        )
        new_patient = Patient.objects.create(
            basic_id=new_patient_info.id,
        )

        new_patient_info.set_password(password)
        new_patient_address.save()
        new_patient_info.save()
        new_patient.save()
        new_patient.hospital.add(context['hospital'])
        print(new_patient_info.username, password)
        context = {'username': new_patient_info.username, "password": password}
        return context

    def save_pharmacist(self, context):
        password = User.objects.make_random_password()
        count = User.objects.count()
        new_pharmacist_address = Address.objects.create(
            region=self.cleaned_data.get('region'),
            zone=self.cleaned_data.get('zone'),
            woreda=self.cleaned_data.get('woreda'),
            kebele=self.cleaned_data.get('kebele'),
            house_no=self.cleaned_data.get('house_no'),
        )
        full_name = self.cleaned_data.get('firstname') + ' ' + self.cleaned_data.get(
            'lastname') + ' ' + self.cleaned_data.get('middlename')
        username = (generate_username(full_name))
        new_pharmacist_info = User.objects.create(
            first_name=self.cleaned_data.get('firstname'),
            last_name=self.cleaned_data.get('lastname'),
            middle_name=self.cleaned_data.get('middlename'),
            email=self.cleaned_data.get('email'),
            sex=self.cleaned_data.get('sex'),
            age=self.cleaned_data.get('age'),
            address_id=new_pharmacist_address.id,
            phone=self.cleaned_data.get('phone'),
            role="pharmacist",
            username=username,

        )

        new_pharmacist = Pharmacist.objects.create(
            basic_id=new_pharmacist_info.id,
            pharmacy_id=context['pharmacy'].id,
        )

        new_pharmacist_info.set_password(password)
        new_pharmacist_address.save()
        new_pharmacist_info.save()
        new_pharmacist.save()
        print(new_pharmacist_info.username, password)
        context = {'username': new_pharmacist_info.username, "password": password}
        return context

    def save(self, context):
        password = User.objects.make_random_password()
        count = User.objects.count()
        new_staff_address = Address.objects.create(
            region=self.cleaned_data.get('region'),
            zone=self.cleaned_data.get('zone'),
            woreda=self.cleaned_data.get('woreda'),
            kebele=self.cleaned_data.get('kebele'),
            house_no=self.cleaned_data.get('house_no'),
        )
        r = None
        s = None

        if self.cleaned_data.get('role') == 'Oncology':
            r = 'Physician'
            s = self.cleaned_data.get('role')
        elif self.cleaned_data.get('role') == 'Internal medicine':
            r = 'Physician'
            s = self.cleaned_data.get('role')
        elif self.cleaned_data.get('role') == 'X-ray':
            r = 'Radiologist'
            s = self.cleaned_data.get('role')
        elif self.cleaned_data.get('role') == 'Ultrasound':
            r = 'Radiologist'
            s = self.cleaned_data.get('role')
        elif self.cleaned_data.get('role') == 'Pediatrics':
            r = 'Physician'
            s = self.cleaned_data.get('role')
        elif self.cleaned_data.get('role') == 'Dermatology':
            r = 'Physician'
            s = self.cleaned_data.get('role')
        elif self.cleaned_data.get('role') == 'Ophthalmology':
            r = 'Physician'
            s = self.cleaned_data.get('role')
        elif self.cleaned_data.get('role') == 'Obstetrics':
            r = 'Physician'
            s = self.cleaned_data.get('role')
        elif self.cleaned_data.get('role') == 'Lab_technician':
            r = 'Lab_technician'
            s = 'Lab_technician'
        else:
            r = self.cleaned_data.get('role')
            s = None
        print(r)
        print(s)
        print(self.cleaned_data.get('role'))

        full_name = self.cleaned_data.get('firstname') + ' ' + self.cleaned_data.get(
            'lastname') + ' ' + self.cleaned_data.get('middlename')
        username = (generate_username(full_name))
        new_staff_basic = User.objects.create(
            first_name=self.cleaned_data.get('firstname'),
            last_name=self.cleaned_data.get('lastname'),
            middle_name=self.cleaned_data.get('middlename'),
            email=self.cleaned_data.get('email'),
            sex=self.cleaned_data.get('sex'),
            address_id=new_staff_address.id,
            age=self.cleaned_data.get('age'),
            phone=self.cleaned_data.get('phone'),
            username=username,
            role=r,
        )
        staff = Staff.objects.create(
            basic_id=new_staff_basic.id,
            hospital_id=context['hospital'].id,
            specialty=s,
        )
        staff.save()
        new_staff_basic.set_password(password)
        new_staff_basic.save()
        new_staff_address.save()

        print(new_staff_basic.username, password)
        context = {'username': new_staff_basic.username, "password": password}
        return context

    def save_admin(self, admin_type):

        password = User.objects.make_random_password()
        count = User.objects.count()
        new_user_address = Address.objects.create(
            region=self.cleaned_data.get('region'),
            zone=self.cleaned_data.get('zone'),
            woreda=self.cleaned_data.get('woreda'),
            kebele=self.cleaned_data.get('kebele'),
            house_no=self.cleaned_data.get('house_no'),
        )
        full_name = self.cleaned_data.get('firstname') + ' ' + self.cleaned_data.get(
            'lastname') + ' ' + self.cleaned_data.get('middlename')
        username = (generate_username(full_name))
        new_user = User.objects.create(
            first_name=self.cleaned_data.get('firstname'),
            last_name=self.cleaned_data.get('lastname'),
            middle_name=self.cleaned_data.get('middlename'),
            email=self.cleaned_data.get('email'),
            sex=self.cleaned_data.get('sex'),
            age=self.cleaned_data.get('age'),
            address_id=new_user_address.id,
            phone=self.cleaned_data.get('phone'),
            username=username,
            role=admin_type,

        )

        new_user.set_password(password)
        new_user_address.save()
        new_user.save()
        print(new_user.username, password)
        context = {'username': new_user.username, "password": password, "admin_id": new_user.id}
        return context
