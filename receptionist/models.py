import datetime

from django.db import models

# Create your models here.
from accounts.models import User, Hospital
from patient.models import Patient


class Triage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    receptionist_id = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    triage_date = models.DateTimeField()

    def __str__(self):
        return Patient.basic.firstname
