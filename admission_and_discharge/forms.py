from django import forms

from accounts.models import Staff
from physician.models import Referral


class DepartmentSelectionForm(forms.Form):
    department = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)  # store value of request
        super(DepartmentSelectionForm, self).__init__(*args, **kwargs)
        print(self.pk)
        self.fields['department'].choices = self.pk
