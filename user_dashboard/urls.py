from django.urls import path
from user_dashboard import views

app_name = "userdashboard"
 
urlpatterns = [
    path("profile", views.profile, name= "profile"),
    path('hotel-profile/', views.hotel_profile, name='hotel_profile'),
    path('update-profile-image/', views.update_profile_image, name='update_profile_image'),
    path('delete-profile-image/', views.delete_profile_image, name='delete_profile_image'),
    path('coupon/', views.coupon, name='coupon'),
    path('change-password/', views.change_password, name='change_password'),
]