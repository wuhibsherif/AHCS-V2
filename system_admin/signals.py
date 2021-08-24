from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from django.dispatch import receiver

@receiver(user_logged_in)
def log_user_logged_in(sender,request,user,**kwargs):
    print(request)
    print("user_logged_in")

@receiver(user_logged_out)
def log_user_logged_out(sender,request,user,**kwargs):
    print(request)
    print("user_logged_out")
@receiver(user_login_failed)
def log_user_logged_failed(sender,request,user,**kwargs):
    print(user)
    print("user_logged_failed")