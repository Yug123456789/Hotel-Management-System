from django.shortcuts import render
from hotel.models import Hotel
from userauthentication.models import Profile
from hotel.models import Bookmark
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages

def profile (request):
    profile = Profile.objects.get(user=request.user)

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