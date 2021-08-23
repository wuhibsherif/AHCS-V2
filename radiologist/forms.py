from django import forms


class XrayResultForm(forms.Form):
    impression = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)
    x_ray_image = forms.ImageField(required=True)


class UltraSoundResultForm(forms.Form):
    sonographic_report = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)
    ultrasound_image = forms.ImageField(required=True)
