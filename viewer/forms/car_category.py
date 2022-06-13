from django import forms
from viewer.models import CarCategory


class CarCategoryForm(forms.ModelForm):
    class Meta:
        model = CarCategory
        fields = '__all__'

    name = forms.CharField(max_length=30)
