from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib import messages
from accounts.models import User
from login import decorators
from login.decorators import allowed_users
from .forms import *


## from django.template.loader import render_to_string
## import weasyprint
from xhtml2pdf import pisa


# @decorators.hospital_adminonly
@login_required(login_url='login_url')
def hospital_admin_homepage(request):
    hospital = Hospital.objects.get(admin=request.user.id)
    request.session['healthcare_name'] = hospital.name
    context = {'hospital_name': hospital}
    return render(request, 'hospital_admin/homepage.html', context)


##############################################################################################################################################
@login_required(login_url='login_url')
def add_new_user(request):
    msg = None
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        hospital = Hospital.objects.get(admin_id=request.user.id)
        context = {'hospital': hospital}
        if form.is_valid():
            new_user = form.save(context)
            messages.success(request, "Staff registered Successfully")

            msg = "Staff registered"
            context = {'username': new_user['username'], 'password': new_user['password']}
            template_path = 'hospital_admin/credentials.html'
            #Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            ## if want to download it
            response['Content-Disposition'] = 'attachment; filename=context["username"]'
            #if want to display it
            #response['Content-Disposition'] = 'filename=context["username"].pdf'
            #find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            #if error then show some funy view

            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    else:
        form = UserRegistrationForm

    context = {'form': form}
    return render(request, 'hospital_admin/receptionists_add.html', context)


################################################################################

# all users
@login_required(login_url='login_url')
@allowed_users(allowed_roles=['hospital admin'])
def all_users(request):
    hospital_id = Hospital.objects.get(admin_id=request.user.id).id
    staffs = Staff.objects.filter(hospital_id=hospital_id)
    context = {'staffs': staffs}
    return render(request, 'forms/all_users.html', context)

    '''receptionists = Receptionist.objects.filter(hospital_id=hospital_id)
    physician = Physician.objects.filter(hospital_id=hospital_id)
    Lab_technician = LabTechnician.objects.filter(hospital_id=hospital_id)
    nurse = Nurse.objects.filter(hospital_id=hospital_id)
    nurse = Radiologist.objects.filter(hospital_id=hospital_id)'''



@login_required(login_url='login_url')
@allowed_users(allowed_roles=['hospital admin'])
def all_physicians(request):
    staff = Staff.objects.filter(hospital_id=Hospital.objects.get(admin_id=request.user.id).id)
    context = {'staff': staff}
    return render(request, 'forms/all-physicians.html', context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['hospital admin'])
def all_nurses(request):
    staff = Staff.objects.filter(hospital_id=Hospital.objects.get(admin_id=request.user.id).id)
    context = {'staff': staff}
    return render(request, 'forms/all-nurses.html', context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['hospital admin'])
def all_radiologists(request):
    staff = Staff.objects.filter(hospital_id=Hospital.objects.get(admin_id=request.user.id).id)
    context = {'staff': staff}
    return render(request, 'forms/all-radiologists.html', context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['hospital admin'])
def all_lab_technicians(request):
    staff = Staff.objects.filter(hospital_id=Hospital.objects.get(admin_id=request.user.id).id)
    context = {'staff': staff}
    return render(request, 'forms/all-lab_technicians.html', context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['hospital admin'])
def all_pharmacists(request):
    all_lab_technician = User.objects.filter(role='Pharmacist')
    context = {'all_pharmacists': all_pharmacists}
    return render(request, 'forms/all-pharmacists.html', context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['hospital admin'])
def all_receptionists(request):
    staff = Staff.objects.filter(hospital_id=Hospital.objects.get(admin_id=request.user.id).id)
    context = {'receptionists': staff}
    return render(request, 'forms/all_receptionists.html', context)
