from datetime import timezone, datetime

from django.db import models
from accounts.models import Hospital, Staff

# Create your models here.
from patient.models import Patient


class PatientWaitingList(models.Model):
    added_by = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='added_by')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    physician = models.ForeignKey(Staff, on_delete=models.CASCADE)
    physician_speciality = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    added_date = models.DateTimeField(auto_now_add=True)
    approval_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.patient


class Appointment(models.Model):
    physician = models.ForeignKey(Staff, on_delete=models.CASCADE, )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, )
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)
    booked_date = models.DateTimeField()
    appointment_date = models.DateTimeField(null=True)
    case = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='pending')


class Referral(models.Model):
    referred_by = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='referred_by')
    referring_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='referring_hospital')
    referred_to_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='referred_to_hospital')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    referral_date = models.DateTimeField()
    approved_on_date = models.DateTimeField(null=True)
    health_problem_identified_in_detail = models.TextField(null=True)
    identified_disease_type = models.CharField(max_length=50, null=True)
    action_taken = models.CharField(max_length=50, null=True)
    reason_for_referral = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, default='pending')
    department = models.CharField(max_length=50, default=None, null=True)
    feedback = models.TextField(null=True)
    feedback_given_by = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, related_name='feedback_given_by')
    approved_by = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, related_name='referral_approved_by')
