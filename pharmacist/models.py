from django.db import models

# Create your models here.
from accounts.models import User, Pharmacy


class Pharmacist(models.Model):
    basic = models.ForeignKey(User, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)

