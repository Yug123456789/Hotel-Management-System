from django import forms
from hotel.models import Hotel, RoomType, Room, Resturant, Coupon
from django.utils import timezone

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'image',  'address', 'mobile', 'email', 'status', 'tags', 'featured', 'hid']


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['hotel', 'type', 'price', 'room_capacity', 'number_of_beds', 'rtid']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hotel', 'room_type', 'room_number', 'is_available', 'rid']

class ResturantForm(forms.ModelForm):
    class Meta:
        model = Resturant
        fields = ['hotel', 'table_number', 'image', 'is_available', 'number_of_seats', 'table_capacity', 'resturantid']



class CouponForm(forms.ModelForm):
    valid_from = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now
    )
    valid_upto = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now() + timezone.timedelta(days=30)
    )
    
    class Meta:
        model = Coupon
        fields = ['hotel', 'code', 'discount', 'type', 'valid_from', 'valid_upto', 'active', 'coupon_id']
        
    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get('valid_from')
        valid_upto = cleaned_data.get('valid_upto')
        
        if valid_from and valid_upto and valid_from >= valid_upto:
            raise forms.ValidationError("The validity end date must be after the start date.")
            
        return cleaned_data