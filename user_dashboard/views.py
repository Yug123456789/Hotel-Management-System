from django.shortcuts import render
from hotel.models import Hotel
from userauthentication.models import Profile
from hotel.models import Bookmark, Coupon
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from userauthentication.forms import CustomPasswordChangeForm
import os
from django.conf import settings

def profile (request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to login first")
        return redirect('userauthentication:sign-in')
    profile = Profile.objects.get(user=request.user)
    print(profile.verified)
    context = {
        'profile': profile,
    }
    return render(request, 'user_dashboard/profile.html', context)


def update_profile_image(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        image = request.FILES.get('image')
        
        if image:
            profile.image = image
            profile.save()
            messages.success(request, 'Profile image updated successfully!')
        else:
            messages.error(request, 'Please select a valid image file.')
    
    return redirect('userdashboard:profile')


def delete_profile_image(request):
    """Delete the user's profile image and reset to default"""
    if not request.user.is_authenticated:
        messages.warning(request, "You have to login first")
        return redirect('userauthentication:sign-in')
    
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        
        # Check if user has a custom image (not the default)
        if profile.image and profile.image.name != 'default.jpg':
            # Get the file path
            image_path = profile.image.path
            
            # Delete the physical file if it exists
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                    messages.success(request, 'Profile image deleted successfully!')
                except Exception as e:
                    messages.error(request, 'Error deleting image file.')
            
            # Reset to default image
            profile.image = 'default.jpg'
            profile.save()
            
        else:
            messages.info(request, 'You are already using the default profile image.')
    
    return redirect('userdashboard:profile')


def hotel_profile(request):
    if request.user.role != 'hotel':
        messages.warning(request, "You are not authorized to access the hotel profile.")
        return redirect('hotel:index')
    
    profile = request.user.profile
    
    context = {
        'profile': profile
    }
    
    return render(request, "user_dashboard/hotel_profile.html", context)

def coupon(request):
    current_time = timezone.now()
    context = {
        "coupons" :  Coupon.objects.filter(
        active=True,
        valid_from__lte=current_time,
        valid_upto__gte=current_time
    )
    }
        
    return render(request, "user_dashboard/coupon.html", context)

def change_password(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to login first")
        return redirect('userauthentication:sign-in')
        
    if request.method == 'POST':
        #If the method iss post the django built in method matches the old password and if it is 
        #correct and the new password match the password credintialks the form will be saveed.
        
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged even after changing the password
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('userdashboard:profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomPasswordChangeForm(request.user)
        
    context = {
        'form': form,
        'profile': Profile.objects.get(user=request.user)
    }
    return render(request, 'user_dashboard/change_password.html', context)