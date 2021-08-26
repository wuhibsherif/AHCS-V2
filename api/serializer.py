from rest_framework.serializers import ModelSerializer

from accounts.models import User, Hospital
from patient.models import *
from physician.models import Appointment



class PrescritionSerializer(ModelSerializer):
    class Meta:
        model= Prescription
        fields='__all__'

class AppointmentSerializer(ModelSerializer):
    class Meta:
        model=Appointment
        fields='__all__'
class UsernameSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username']

class HospitalSerializer(ModelSerializer):
    class Meta:
        model:Hospital
        fields='__all__'