from django.urls import path
from booking import views

app_name = "booking"


urlpatterns = [
    path("check_room_availability/", views.check_room_availability, name = "check_room_availability"),
    path("check_resturant_availability/", views.check_resturant_availability, name = "check_resturant_availability"),
    path("add_to_selection/", views.add_to_selection, name = "add_to_selection"),
    path("add_to_resturant_selection/", views.add_to_resturant_selection, name = "add_to_resturant_selection"),
    path("remove_selection/", views.remove_selection, name = "remove_selection"),
]
