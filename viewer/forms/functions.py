from django import forms
from .car_category import CarCategory
from viewer.models import Rental



class Availability(forms.Form):

    CATEGORY = [item for item in CarCategory.objects.all()]

    TRANSMISSION = [
        ('Manualna', 'Manualna'),
        ('Automat', 'Automat')
    ]
    rental = forms.ModelChoiceField(label='city',queryset=Rental.objects)
    category = forms.ModelChoiceField(label='category', queryset=CarCategory.objects, required=False )
    transmission = forms.ChoiceField(label='transmission', choices=TRANSMISSION)
    air_conditioning = forms.BooleanField(required=False)
    date_of_rental = forms.DateField(widget=forms.SelectDateWidget, label= 'date_of_rental', required=True)
    date_of_return = forms.DateField(widget=forms.SelectDateWidget, label= 'date_of_return', required=True)