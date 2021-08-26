from django.contrib.auth.models import AbstractUser
from django.db import models
from django_cryptography.fields import encrypt

# Create your models here.


class Address(models.Model):
    region = models.CharField(max_length=150)
    zone = models.CharField(max_length=50)
    woreda = models.CharField(max_length=50)
    kebele = models.CharField(max_length=50)
    house_no = encrypt(models.CharField(max_length=50))

    def __str__(self):
        return self.wereda


class User(AbstractUser):
    middle_name = models.CharField(max_length=20)
    age = models.CharField(max_length=50)
    sex = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username


class Hospital(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Pharmacy(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    basic = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=50, null='true', default='no specialty')
    num_waiting = models.IntegerField(default=0)

    def __str__(self):
        return User.username
