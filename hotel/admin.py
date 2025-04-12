from django.contrib import admin
from hotel.models import (
    Hotel, HotelGallery, HotelFeatures, HotelFaqs, RoomType, Room, 
    Resturant, Booking, ActivityLog, StaffOnDuty, Coupon, ResturantBooking
)

# Custom admin for Hotel
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'thumbnail', 'owner', 'status']
    readonly_fields = ['thumbnail']
    prepopulated_fields = {"slug": ('name',)}
    search_fields = ['name', 'user__username']
    list_filter = ['status', 'featured', 'date']

# Custom admin for Room Type
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'hotel', 'price', 'room_capacity', 'number_of_beds']
    search_fields = ['type', 'hotel__name']
    list_filter = ['hotel']

# Custom admin for Room
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'hotel', 'room_type', 'is_available']
    list_filter = ['hotel', 'room_type', 'is_available']
    search_fields = ['room_number', 'hotel__name', 'room_type__type']

# Custom admin for Hotel Gallery
class HotelGalleryAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'image']
    list_filter = ['hotel']

# Custom admin for Hotel Features
class HotelFeaturesAdmin(admin.ModelAdmin):
    list_display = ['name', 'hotel', 'icon_type', 'icon']
    search_fields = ['name', 'hotel__name']
    list_filter = ['icon_type']

# Custom admin for Hotel FAQs
class HotelFaqsAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'question']
    search_fields = ['question', 'hotel__name']
    list_filter = ['date']

# Custom admin for Restaurant
class ResturantAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'table_number', 'is_available', 'number_of_seats']
    search_fields = ['hotel__name', 'table_number']
    list_filter = ['hotel', 'is_available']

# Custom admin for Booking
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'hotel',  'room_type', 'payment_status', 'check_in_date', 'check_out_date']
    list_filter = ['payment_status', 'check_in_date', 'check_out_date']
    search_fields = ['booking_id', 'user__username', 'hotel__name', 'room_type__type']

class ResturantBookingAdmin(admin.ModelAdmin):
    list_display = [
        'rbooking_id', 'full_name', 'email', 'phone', 
        'user', 'hotel', 
        'check_in_date', 'check_in_time', 'check_out_time'
    ]
    list_filter = ['hotel',  'check_in_date']
    search_fields = [
        'rbooking_id', 'full_name', 'email', 'phone', 
        'user__username', 'hotel__name'
    ]

# Custom admin for Activity Log
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['booking', 'guest_out', 'guest_in', 'description', 'date']
    list_filter = ['date']
    search_fields = ['booking__booking_id']

# Custom admin for Staff On Duty
class StaffOnDutyAdmin(admin.ModelAdmin):
    list_display = ['booking', 'staff_id', 'date']
    search_fields = ['staff_id', 'booking__booking_id']

# Custom admin for Coupon
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'type', 'valid_from', 'valid_upto', 'active']
    search_fields = ['code']
    list_filter = ['active', 'valid_from', 'valid_upto']

# Register models with custom admin classes
admin.site.register(Hotel, HotelAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(HotelGallery, HotelGalleryAdmin)
admin.site.register(HotelFeatures, HotelFeaturesAdmin)
admin.site.register(HotelFaqs, HotelFaqsAdmin)
admin.site.register(Resturant, ResturantAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(ActivityLog, ActivityLogAdmin)
admin.site.register(StaffOnDuty, StaffOnDutyAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(ResturantBooking, ResturantBookingAdmin)