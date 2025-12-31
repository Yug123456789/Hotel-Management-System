from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # If user is superuser (admin)
            if request.user.is_superuser:
                # Prevent access to user-side pages (except admin pages)
                if not request.path.startswith('/admin/'):
                    messages.warning(request, "Admins cannot access user pages.")
                    return redirect(reverse('admin:index'))
            else:
                # If user is not superuser, prevent access to admin pages
                if request.path.startswith('/admin/'):
                    messages.warning(request, "You cannot access admin panel.")
                    return redirect('hotel:index')

        return self.get_response(request)
