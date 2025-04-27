from django.shortcuts import render
from hotel.models import Hotel
from userauthentication.models import Profile
from hotel.models import Bookmark, Coupon
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone


def profile (request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to loin first")
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
