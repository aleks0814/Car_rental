from django import forms
from viewer.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    login = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=30)
    document_id = forms.CharField(max_length=30)


class ClientSelect(forms.Form):
    client = forms.ModelChoiceField(Client.objects)
