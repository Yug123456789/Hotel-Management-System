from django.urls import path
from hotel import views

app_name = "hotel"
 
urlpatterns = [
    path("", views.index, name= "index"),
    path("detail/<slug>", views.hotel_detail, name= "hotel_detail"),
    path("detail/<slug:slug>/room-type/<slug:roomtype_slug>/", views.room_type_detail, name= "room_type_detail"),
    path("rooms_selected/", views.rooms_selected, name="rooms_selected"),
    path("restaurant_selected/", views.restaurant_selected, name="restaurant_selected"),
    path("checkout/<booking_id>/", views.checkout, name="checkout"),
    path("restaurant_checkout/<booking_id>/", views.restaurant_checkout, name="restaurant_checkout"),
    path("detail/<slug:slug>/resturant2/", views.resturant_table_detail, name="resturant_table_detail"),
    path("detail/<slug>/resturant/", views.resturant, name= "resturant"),
    path('add', views.add_hotels, name='add_hotel'),
    path('add-room-type/', views.add_room_types, name='add_room_type'),
    path('add-room/', views.add_rooms, name='add_room'),
    path('add-restaurant/', views.add_restaurants, name='add_restaurant'),
    path('coupons/add/', views.add_coupons, name='add_coupon'),
    path('user_hotel/', views.user_hotel, name='user_hotel'),
    path('hotel_user_dashboard/', views.user_hotel_dashboard, name='hotel_user_dashboard'),
    
]
