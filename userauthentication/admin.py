from django.contrib import admin
from userauthentication.models import User, Profile

class UserAdmin(admin.ModelAdmin): #Enabling to search Users in Admin page 
    search_fields = ['full_name', 'username']
    list_display = ['username', 'full_name', 'email', 'phone']


class ProfileAdmin(admin.ModelAdmin): #Enabling to search Profiles in Admin page
    search_fields = ['full_name', 'user__username']
    list_display = [ 'full_name', 'user', 'verified']


admin.site.register(User, UserAdmin) #Registering User model
admin.site.register(Profile, ProfileAdmin) #Registering Profile model
