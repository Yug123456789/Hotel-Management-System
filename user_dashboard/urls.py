from django.urls import path
from user_dashboard import views

app_name = "userdashboard"
 
urlpatterns = [
    path("profile", views.profile, name= "profile"),
]