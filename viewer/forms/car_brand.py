from viewer.models import CarBrand
from django import forms


class CarBrandForm(forms.ModelForm):
    class Meta:
        model = CarBrand
        fields = '__all__'

    name = forms.CharField(max_length=30)
