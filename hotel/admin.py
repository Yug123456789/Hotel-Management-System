from django.contrib import admin
from hotel.models import Hotel, HotelGallery, HotelFeatures, HotelFaqs, RoomType, Room, Resturant, Booking, ActivityLog, StaffOnDuty


# Register your models here.

class HotelAdmin(admin.ModelAdmin):
    list_display  = ['name', 'thumbnail', 'user', 'status']
    prepopulated_fields = {"slug": ('name',)}

admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelGallery)
admin.site.register(HotelFeatures)
admin.site.register(HotelFaqs)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Resturant)
admin.site.register(Booking)
admin.site.register(ActivityLog)
admin.site.register(StaffOnDuty)


