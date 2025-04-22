from django.urls import path
from userauthentication import views

app_name = "userauthentication"
 
urlpatterns = [
    path("choose-sign-in/", views.ChooseSignInView, name="choose-sign-in"),
    path("sign-up/", views.RegisterView, name= "sign-up"),
    path("hotel-sign-up/", views.HotelRegisterView, name= "hotel-sign-up"),
    path('login/', views.universal_login_view, name='sign-in'),
    path('hotel-login/', views.universal_login_view, name='hotel-sign-in'),
    path("sign-out/", views.LogoutView, name= "sign-out"),
    
]




