from django.urls import path
from hotel import views

app_name = "hotel"
 
urlpatterns = [
    path("", views.index, name= "index"),
    path("detail/<slug>", views.hotel_detail, name= "hotel_detail"),
    path("detail/<slug:slug>/room-type/<slug:roomtype_slug>/", views.room_type_detail, name= "room_type_detail"),
    path("rooms_selected/", views.rooms_selected, name="rooms_selected"),
    path("checkout/<booking_id>/", views.checkout, name="checkout"),
]
