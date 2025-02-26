from django.urls import path
from userauthentication import views

app_name = "userauthentication"
 
urlpatterns = [
    path("sign-up/", views.RegisterView, name= "sign-up"),
    path("sign-in/", views.loginViewTemp, name= "sign-in"),
    path("sign-out/", views.LogoutView, name= "sign-out"),
]




