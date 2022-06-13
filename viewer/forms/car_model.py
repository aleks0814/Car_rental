from viewer.models import CarModel, CarBrand, CarCategory
from django import forms


class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = '__all__'

    car_category = forms.ModelChoiceField(label='Kategoria auta', queryset=CarCategory.objects, required=True)
    car_brand = forms.ModelChoiceField(label='Marka auta', queryset=CarBrand.objects, required=True)
    name = forms.CharField(label='Nazwa', max_length=30)
    capacity = forms.IntegerField(min_value=1)
    picture = forms.ImageField()
