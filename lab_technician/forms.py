from django import forms

from lab_technician.models import UrineAnalysisWaitingList, HematologyWaitingList
from patient.models import StoolExamination


class StoolResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)  # store value of request
        super(StoolResultForm, self).__init__(*args, **kwargs)
        stool = StoolExamination.objects.filter(patient_id=self.instance['patient'], hospital_id=self.instance['hospital']).latest('date_of_request')
        for field in stool._meta.fields:
            if (getattr(stool, field.name)) == 'requested':
                self.fields[field.name] = forms.CharField(required=True)


class UrineResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)  # store value of request
        super(UrineResultForm, self).__init__(*args, **kwargs)
        urine = UrineAnalysisWaitingList.objects.filter(patient_id=self.instance['patient'], hospital_id=self.instance['hospital']).latest('date_of_request')
        for field in urine._meta.fields:
            if (getattr(urine, field.name)) is True:
                self.fields[field.name] = forms.IntegerField(required=True)


class HematologyResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)  # store value of request
        super(HematologyResultForm, self).__init__(*args, **kwargs)
        urine = HematologyWaitingList.objects.filter(patient_id=self.instance['patient'], hospital_id=self.instance['hospital']).latest('date_of_request')
        for field in urine._meta.fields:
            if (getattr(urine, field.name)) is True:
                self.fields[field.name] = forms.IntegerField(required=True)
