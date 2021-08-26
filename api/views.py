from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import User, Hospital

from .serializer import *
from patient.models import Prescription, Patient
from physician.models import Appointment

# Create your views here.


@api_view(['GET'])

def getMedication(request,username):
    prescription=Prescription.objects.filter(patient_id=Patient.objects.get(basic_id=User.objects.get(username=username).id))
    serializer=PrescritionSerializer(prescription,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def  getAppointment(request,username):
    appointment=Appointment.objects.filter(patient_id=Patient.objects.get(basic_id=User.objects.get(username=username).id))

    serializer=AppointmentSerializer(appointment,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def check(request,username,password):
    username2=username
    password=password
    print(username2)
    username1=User.objects.get(username=username2)
    print(username1)
    serializer=UsernameSerializer(username1,many=False)
    user = authenticate(username=username, password=password)
    if user:
        return Response(serializer.data)


