from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import LoginForm


# Create your views here.
def user_login(request):
    msg = None
    form = LoginForm(request.POST or None)
    print("above request")
    if request.method == 'POST':
        print("post request")
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print("form is valid")
            user = authenticate(username=username, password=password)

            if user is not None and user.is_superuser:
                if user.is_active:
                    login(request, user)
                    return redirect('system_admin_homepage_url')
                else:
                    print("disabled account")

            elif user is not None and user.role == 'hospital admin':
                if user.is_active:
                    login(request, user)
                    return redirect('hospital_admin_homepage_url')
                else:
                    print("disabled account")
            elif user is not None and user.role == 'pharmacy admin':
                if user.is_active:
                    login(request, user)
                    return redirect('pharmacy_admin_homepage_url')
                else:
                    print("disabled account")
            elif user is not None and user.role == 'Receptionist':
                if user.is_active:
                    login(request, user)
                    return redirect('receptionist_homepage_url')
                else:
                    print("disabled account")
            elif user is not None and user.role == 'Physician':
                if user.is_active:
                    login(request, user)
                    return redirect('physician_homepage_url')
                else:
                    print("disabled account")
            elif user is not None and user.role == 'Nurse':
                if user.is_active:
                    login(request, user)
                    return redirect('nurse_homepage_url')
                else:
                    print("disabled account")
            elif user is not None and user.role == 'Radiologist':
                if user.is_active:
                    login(request, user)
                    return redirect('radiologist_homepage_url')
                else:
                    print("disabled account")
            elif user is not None and user.role == 'Lab_technician':
                if user.is_active:
                    login(request, user)
                    return redirect('lab_technician_homepage_url')
                else:
                    print("disabled account")
            elif user is not None and user.role == 'Admission and discharge':
                if user.is_active:
                    login(request, user)
                    return redirect('admission_and_discharge_homepage_url')
                else:
                    print("disabled account")

            elif user is not None and user.role == 'pharmacist':
                if user.is_active:
                    login(request, user)
                    return redirect('pharmacist_homepage_url')
                else:
                    print("disabled account")
            else:
                msg = 'Username Or Password Incorrect'
        else:
            msg = form.errors
    context = {'form': form, 'msg': msg}
    return render(request, 'login_page.html', context)


def user_logout(request):
    logout(request)
    return redirect('login_url')