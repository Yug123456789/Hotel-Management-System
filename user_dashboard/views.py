from django.shortcuts import render
from hotel.models import Hotel
from userauthentication.models import Profile
from hotel.models import Bookmark
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

def profile (request):
    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
    }
    return render(request, 'user_dashboard/profile.html', context)