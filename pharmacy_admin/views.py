from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import User, Pharmacy
from hospital_admin.forms import UserRegistrationForm
from login import decorators


## from django.template.loader import render_to_string
## import weasyprint
# from xhtml2pdf import pisa
from login.decorators import allowed_users


@login_required(login_url='login_url')
@allowed_users(allowed_roles=['pharmacy admin'])
def pharmacy_admin_homepage(request):
    pharmacy = Pharmacy.objects.get(admin=request.user.id)
    request.session['healthcare_name'] = pharmacy.name
    context = {'pharmacy_name': pharmacy}

    return render(request, 'pharmacy_admin/homepage.html', context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['pharmacy admin'])
def all_pharmacists(request):
    all_lab_technician = User.objects.filter(role='Pharmacist')
    context = {'all_pharmacists': all_pharmacists}
    return render(request, 'forms/all-pharmacists.html', context)

@login_required(login_url='login_url')
@allowed_users(allowed_roles=['pharmacy admin'])
def register_pharmacist(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('form is valid')
            pharmacy = Pharmacy.objects.get(admin_id=request.user.id)
            context = {'pharmacy': pharmacy}
            new_user = form.save_pharmacist(context)
            context = {'username': new_user['username'], 'password': new_user['password']}
            '''template_path = 'receptionist/credentials.html'
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            ## if want to download it
            ##response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            ## if want to display it
            response['Content-Disposition'] = 'filename=context["username"].pdf'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response'''

    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'pharmacy_admin/forms/pharmacist_registration_form.html', context)
