from django import forms
from .models import *

class BookTicket(forms.ModelForm):
    class Meta:
        model = BookingForm
        fields = ['firstName','lastName','phone_number','age','country','gender','packs','date']

class orderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = '__all__'
