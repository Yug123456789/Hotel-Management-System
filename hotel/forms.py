from django import forms
from hotel.models import Hotel

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name',   'address', 'mobile', 'email', 'status', 'tags', 'featured', 'hid']
