
from random import choice
from string import ascii_lowercase, digits
from django.contrib.auth.models import User
import random


def generate_random_username(length=4, chars=ascii_lowercase+digits, split=2, delimiter='-'):
    
    username = ''.join([choice(chars) for i in range(length)])
    
    if split:
        username = delimiter.join([username[start:start+split] for start in range(0, len(username), split)])
    
    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username;
    
    
    
def password_generator():
    password=generate_random_username()
    return password

def passwordgen(request):
    
        characters = list('abcdefghilmnopqrstuvz')

        length = int(request.GET.get('length', 8))

        if request.POST.get('uppercase'):
            characters.extend([x.upper() for x in characters])
        if request.POST.get('numbers'):
            characters.extend(list('123456789'))
        if request.POST.get('special'):
            characters.extend(list('./?\|}!@$^&'))


        gen_pas = ''

        for x in range(length):
            gen_pas += random.choice(characters)

        return gen_pas