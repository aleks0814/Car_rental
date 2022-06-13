from viewer.models import Rental
from django import forms


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = '__all__'

    name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=120)
    number_of_cars = forms.IntegerField(min_value=0)

class RentalSelectForm(forms.Form):
    rental = forms.ModelChoiceField(queryset=Rental.objects)

