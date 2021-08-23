import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.utils import timezone

from hospital_admin.forms import *
from xhtml2pdf import pisa
from accounts.models import User

# Create your views here.
from login import decorators
from physician.models import Appointment
from receptionist.models import Triage


@login_required(login_url='login_url')
@decorators.allowed_users(allowed_roles=['Receptionist'])
def receptionist_dashboard(request):
    hospital = Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id)
    request.session['healthcare_name'] = hospital.name
    context = {'hospital': hospital}
    return render(request, "receptionist/homepage.html", context)

@login_required(login_url='login_url')
@decorators.allowed_users(allowed_roles=['Receptionist'])
def register_new_patient(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            hospital = Staff.objects.get(basic_id=request.user.id).hospital.id
            context = {'hospital': hospital}
            new_user = form.save_patient(context)
            username = new_user['username']
            context = {'username': new_user['username'], 'password': new_user['password']}
            template_path = 'receptionist/credentials.html'
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            ## if want to download it
            response['Content-Disposition'] = 'attachment; filename={{username}}.pdf'
            ## if want to display it
            # response['Content-Disposition'] = 'filename={{context["username"]}}.pdf'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response

    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'receptionist/form/registration_form.html', context)

@login_required(login_url='login_url')
@decorators.allowed_users(allowed_roles=['Receptionist'])
def patient_profile(request, pk):
    profile = User.objects.get(id=pk)
    # info = UserInfo.objects.get(user_id=pk)
    print(profile)
    context = {'patient': profile}
    return render(request, 'receptionist/patient_profile.html', context)

    ## group=request.user.groups.all()[0].name

    ##else:

@login_required(login_url='login_url')
@decorators.allowed_users(allowed_roles=['Receptionist'])
def admit_to_triage(request, pk):
    triage_list = Triage.objects.create(
        hospital_id=Hospital.objects.get(id=Staff.objects.get(basic_id=request.user.id).hospital_id).id,
        patient_id=Patient.objects.get(basic_id=pk).id,
        receptionist_id=request.user.id,
        status='pending',
        triage_date=datetime.datetime.now(),
    )
    triage_list.save()
    return redirect('receptionist_homepage_url')

@login_required(login_url='login_url')
@decorators.allowed_users(allowed_roles=['Receptionist'])
def view_appointment(request, pk):
    try:
        appointment = Appointment.objects.get(patient_id=pk, status='pending')
        print(appointment.case)
    except:
        appointment = None

    context = {'appointment': appointment}
    return render(request, 'profiles/receptionist_patient_profile.html', context)
