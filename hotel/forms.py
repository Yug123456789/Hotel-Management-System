from django import forms
from hotel.models import Hotel

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'image',  'address', 'mobile', 'email', 'status', 'tags', 'featured', 'hid']
