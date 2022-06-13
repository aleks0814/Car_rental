from django import forms
from viewer.models import Car, CarModel, Rental


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

    # car_model = forms.ModelChoiceField(widget=CarModel.objects.all())
    car_model = forms.ModelChoiceField(queryset=CarModel.objects, required=True)
    rental = forms.ModelChoiceField(queryset=Rental.objects, required=True)
    transmission = forms.ChoiceField(choices=Car.TRANSMISSION)
    air_conditioning = forms.BooleanField(required=False)
    price_per_day = forms.FloatField(min_value=0)
    avability = forms.BooleanField(required=False)

class CarSelectForm(forms.ModelForm):
    car = forms.ModelChoiceField(queryset=Car.objects)
