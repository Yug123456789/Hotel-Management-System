from django.urls import path
from user_dashboard import views

app_name = "userdashboard"
 
urlpatterns = [
    path("profile", views.profile, name= "profile"),
    path('update-profile-image/', views.update_profile_image, name='update_profile_image'),
]