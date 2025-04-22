from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from shortuuid.django_fields import ShortUUIDField


IDENTITY_TYPE = (
    ("Citizenship Number", "Citizenship Number"),
    ("Passport Number", "Passport Number")
)

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('customer', 'Customer'),
    ('hotel', 'Hotel'),
)

def user_directory_path(instance, filename): #To upload the image of profile model of user
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (instance.user.id, filename)
    return "user_{0}/{1}".format(instance.user.id, filename)


class User(AbstractUser):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.username

class Profile(models.Model):
    profile_id = ShortUUIDField(length=7, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz12345")
    image = models.FileField(upload_to=user_directory_path, default="default.jpg", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # CASCADE automatically deletes the profile whenever a user is deleted. 
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)    
    city = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    identity_type = models.CharField(max_length=100, choices=IDENTITY_TYPE, null=True, blank=True)
    identity_image = models.FileField(upload_to=user_directory_path, default="id.jpg", null=True, blank=True)
    verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"
        else:
            return f"{self.user.username}"

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

