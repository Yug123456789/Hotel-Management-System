from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from userauthentication.models import User
from shortuuid.django_fields import ShortUUIDField
from taggit.managers import TaggableManager
import shortuuid

HOTEL_STATUS = (
    ("Draft", "Draft"),
    ("Disabled", "Disabled"),
    ("Rejected", "Rejected"),
    ("Live", "Live"),
    
)

ICON_TYPE = (
    ("Bootstrap Icons", "Bootstrap Icons"),
    ("Fontawesome Icons", "Fontawesome Icons"), 
    ("Remi Icons", "Remi Icons"),    
)

PAYMENT_STATUS = (
    ("Paid ", "Paid "),
    ("Pending ", "Pending "), 
    ("Processing ", "Processing "),    
    ("Cancelled ", "Cancelled "),    
    ("Failed ", "Failed "),    
    ("Refunding ", "Refunding "),   
    ("Refunded ", "Refunded "),     
    ("Unpaid ", "Unpaid "),    
    ("Expired ", "Expired "),    
)



# Create your models here.

class Hotel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150,null=True)
    description = models.CharField(max_length=10000, null=True, blank=True)
    image = models.ImageField(upload_to='aa', blank=True,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=50,null=True)
    status = models.CharField(max_length=50, choices=HOTEL_STATUS, default="Live")
    tags = TaggableManager(blank=True)
    views = models.IntegerField(default=0,null=True)
    hid = ShortUUIDField(unique=True, length = 8, max_length=15, alphabet = "abcdefghijklmnopqrstuvwxyz",null=True)
    featured = models.BooleanField(default=False,null=True)
    slug = models.SlugField(unique=True,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            uuid_key = shortuuid.uuid()  
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.name) + '-' + str(uniqueid.lower())
        super(Hotel, self).save(*args, **kwargs)

    def thumbnail(self):
        if self.image and hasattr(self.image, 'url'):
            return mark_safe(f"<img src='{self.image.url}' width='50' height='50' style='object-fit: cover; border-radius: 7px;' />")
        else:
            return mark_safe("<img src='/static/images/club_himalayan.jpeg' width='50' height='50' style='object-fit: cover; border-radius: 7px;' />")
    
    def hotel_room_types(self):
        return RoomType.objects.filter(hotel=self)

class HotelGallery(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete= models.CASCADE)    
    image = models.FileField(upload_to ="hotel_gallery")
    hgid = ShortUUIDField(unique=True, length = 8, max_length=15, alphabet = "abcdefghijklmnopqrstuvwxyz")

    def __str__(self):
        return str(self.hotel.name)
    
    class Meta:
        verbose_name_plural = "Hotel Gallery"

class HotelFeatures(models.Model):  
    hotel = models.ForeignKey(Hotel, on_delete= models.CASCADE)
    icon_type = models.CharField(max_length=150, null=True, blank=True, choices=ICON_TYPE)   
    icon = models.CharField(max_length=150, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Hotel Features"

class HotelFaqs(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete= models.CASCADE)
    question = models.CharField(max_length=1500)
    answer = models.CharField(max_length=1500, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question)
    
    class Meta:
        verbose_name_plural = "Hotel FAQS"


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete= models.CASCADE)
    type = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    room_capacity = models.PositiveBigIntegerField(default=0)
    number_of_beds = models.PositiveBigIntegerField(default=0)
    rtid = ShortUUIDField(unique=True, length = 8, max_length=15, alphabet = "abcdefghijklmnopqrstuvwxyz")
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.hotel.name} - {self.price}"
    
    class Meta:
        verbose_name_plural = "Room Type"

    def rooms_count(self):
        Room.objects.filter(room_type=self).count()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.type) + '-' + str(uniqueid.lower()) 
        super(RoomType, self).save(*args, **kwargs)

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete= models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete= models.CASCADE)
    room_number = models.CharField(max_length=150)
    is_available = models.BooleanField(default=True)
    rid = ShortUUIDField(unique=True, length = 8, max_length=15, alphabet = "abcdefghijklmnopqrstuvwxyz")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_type.type} - {self.hotel.name}"
    
    class Meta:
        verbose_name_plural = "Rooms"

    def price(self):
        return self.room_type.price

    def number_of_beds(self):
        return self.room_type.number_of_beds
    
class Resturant(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete= models.CASCADE)
    table_number = models.CharField(max_length=150)
    
    is_available = models.BooleanField(default=True)
    number_of_seats = models.IntegerField(default=0)
    table_capacity = models.IntegerField(default=0)
    resturantid = ShortUUIDField(unique=True, length = 8, max_length=15, alphabet = "abcdefghijklmnopqrstuvwxyz")
    date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.table_number} - {self.hotel.name}"
    
    class Meta:
        verbose_name_plural = "Resturants"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True, blank=True)
    payment_status = models.CharField(max_length=150, choices = PAYMENT_STATUS)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=150)
    coupons = models.ManyToManyField("hotel.Coupon", blank=True)

    hotel = models.ForeignKey(Hotel, on_delete= models.SET_NULL, null=True, blank=True)
    
    room_type = models.ForeignKey(RoomType, on_delete= models.SET_NULL, null=True, blank=True)
    room = models.ManyToManyField(Room)
    before_discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    saved_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_days = models.PositiveIntegerField(default=0)
    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)
            

    is_active = models.BooleanField(default=False)
    checked_in_tracker = models.BooleanField(default=False)
    checked_out_tracker = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    khalti_payment = models.CharField(max_length=1000, null=True, blank=True)
    success_id = models.CharField(max_length=1000, null=True, blank=True)
    booking_id = ShortUUIDField(unique=True, length = 8, max_length=15, alphabet = "abcdefghijklmnopqrstuvwxyz")
 
    
    def __str__(self):
        return f"{self.booking_id}"

    def rooms(self):
        return self.room.all().count()
    
class ResturantBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tables = models.ManyToManyField(Resturant, related_name='restaurant_table_bookings')
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=150)
    check_in_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    total_time = models.FloatField(null=True, blank=True)
   
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    

    rbooking_id = ShortUUIDField(unique=True, length=8, max_length=15, alphabet="abcdefghijklmnopqrstuvwxyz")

    def __str__(self):
        return f"{self.rbooking_id}"


class ActivityLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    guest_out = models.DateTimeField()
    guest_in = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.booking}"

class StaffOnDuty(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.staff_id}"


class Coupon(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete= models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=2000)
    discount = models.IntegerField(default=1)
    type = models.CharField(max_length=200, default="Percentage")
    date = models.DateTimeField(auto_now_add=True)
    valid_from = models.DateTimeField()
    valid_upto = models.DateTimeField()
    coupon_id = ShortUUIDField(unique=True, length = 8, max_length=15, alphabet = "abcdefghijklmnopqrstuvwxyz")
    active = models.BooleanField(default=True)

  
    def __str__(self):
        return f"{self.code}"