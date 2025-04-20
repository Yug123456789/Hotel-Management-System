from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from urllib.parse import urlencode
from datetime import datetime
from hotel.models import Hotel, HotelGallery,   RoomType, Room, Resturant, Booking, ActivityLog, StaffOnDuty
from django.template.loader import render_to_string

def check_room_availability(request):
    if request.method == "POST":
        id = request.POST.get("hotel-id")
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")
        
        room_type_slug = request.POST.get("room_type")  

        try:
            hotel = Hotel.objects.get(id=id)
            room_type = RoomType.objects.get(hotel=hotel, slug=room_type_slug)
        except (Hotel.DoesNotExist, RoomType.DoesNotExist):
            return HttpResponseRedirect(reverse("booking:home"))  # Redirect if not found

        print("id ===", id)
        print("checkin ===", checkin)
        print("checkout ===", checkout)
        print("room_type ===", room_type)
        print("hotel ===", hotel)
        print("room_type ===", room_type)

        url = reverse("hotel:room_type_detail", args=[hotel.slug, room_type.slug])
        query_params = urlencode({
            "hotel-id": id,
            "checkin": checkin,
            "checkout": checkout,
            "room_type": room_type.slug  
        })

        return HttpResponseRedirect(f"{url}?{query_params}")
    
def hotel_user_check_room_availability(request):
    if request.method == "POST":
        id = request.POST.get("hotel-id")
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")
        
        room_type_slug = request.POST.get("room_type")  

        try:
            hotel = Hotel.objects.get(id=id)
            room_type = RoomType.objects.get(hotel=hotel, slug=room_type_slug)
        except (Hotel.DoesNotExist, RoomType.DoesNotExist):
            return HttpResponseRedirect(reverse("booking:home"))  # Redirect if not found

        print("id ===", id)
        print("checkin ===", checkin)
        print("checkout ===", checkout)
        print("room_type ===", room_type)
        print("hotel ===", hotel)
        print("room_type ===", room_type)

        url = reverse("hotel:user_hotel_room_type_detail", args=[hotel.slug, room_type.slug])
        query_params = urlencode({
            "hotel-id": id,
            "checkin": checkin,
            "checkout": checkout,
            "room_type": room_type.slug  
        })

        return HttpResponseRedirect(f"{url}?{query_params}")
    
def check_resturant_availability(request):
    if request.method == "POST":
        id = request.POST.get("hotel-id")
        checkin = request.POST.get("checkin")
        
        checkintime = request.POST.get("checkintime")
        checkouttime = request.POST.get("checkouttime")
        
        try:
            hotel = Hotel.objects.get(id=id)
            
        except (Hotel.DoesNotExist):
            return HttpResponseRedirect(reverse("booking:home"))  # Redirect to home page of hotel app if not found

        print("id ===", id)
        print("checkin ===", checkin)
        
        print("checkintime ===", checkintime)
        print("checkouttime ===", checkouttime)
        
        print("hotel ===", hotel)
        

        url = reverse("hotel:resturant_table_detail", args=[hotel.slug])
        query_params = urlencode({
            "hotel-id": id,
            "checkin": checkin,
            
            "checkintime": checkintime,
            "checkouttime": checkouttime,
              
        })

        return HttpResponseRedirect(f"{url}?{query_params}")
    

def hotel_user_check_resturant_availability(request):
    if request.method == "POST":
        id = request.POST.get("hotel-id")
        checkin = request.POST.get("checkin")
        
        checkintime = request.POST.get("checkintime")
        checkouttime = request.POST.get("checkouttime")
        
        try:
            hotel = Hotel.objects.get(id=id)
            
        except (Hotel.DoesNotExist):
            return HttpResponseRedirect(reverse("booking:home"))  # Redirect to home page of hotel app if not found

        print("id ===", id)
        print("checkin ===", checkin)
        
        print("checkintime ===", checkintime)
        print("checkouttime ===", checkouttime)
        
        print("hotel ===", hotel)
        

        url = reverse("hotel:user_hotel_resturant_table_detail", args=[hotel.slug])
        query_params = urlencode({
            "hotel-id": id,
            "checkin": checkin,
            
            "checkintime": checkintime,
            "checkouttime": checkouttime,
              
        })

        return HttpResponseRedirect(f"{url}?{query_params}")

def add_to_selection(request):
    room_selection = {}

    room_id = str(request.GET.get('id', ''))  # Ensure room_id is a string

    room_selection[room_id] = {
        'hotel_id': request.GET.get('hotel_id', ''),
        'hotel_name': request.GET.get('hotel_name', ''),
        'room_name': request.GET.get('room_name', ''),
        'room_price': request.GET.get('room_price', ''),
        'room_number': request.GET.get('room_number', ''),
        'room_type': request.GET.get('room_type', ''),
        'room_id': request.GET.get('room_id', ''),
        'number_of_beds': request.GET.get('number_of_beds', ''),
        'checkin': request.GET.get('checkin', ''),  # Get checkin date
        'checkout': request.GET.get('checkout', ''),  # Get checkout date
    }

    if 'selection_data_object' in request.session:
        selection_data = request.session['selection_data_object']
        room_id = str(request.GET.get('id', ''))  # Use .get() to avoid KeyError

        if room_id in selection_data:  
            # Ensure the keys exist before modifying them
            selection_data[room_id]['checkin'] = room_selection.get(room_id, {}).get('checkin', '')
            selection_data[room_id]['checkout'] = room_selection.get(room_id, {}).get('checkout', '')
        else:
            selection_data.update(room_selection)  # Add new room if not in session

        request.session['selection_data_object'] = selection_data
        request.session.modified = True  # Force session update

    else:
        request.session['selection_data_object'] = room_selection
        request.session.modified = True

    data = {
        'data': request.session['selection_data_object'],
        "total_selected_items": len(request.session['selection_data_object']),
    }

    return JsonResponse(data)


def add_to_resturant_selection(request):
    resturant_selection = {}

    restaurant_id = str(request.GET.get('restaurant_id', ''))  # Ensure restaurant_id is a string

    resturant_selection[restaurant_id] = {
        'hotel_id': request.GET.get('hotel_id', ''),
        'hotel_name': request.GET.get('hotel_name', ''),
        'restaurant_id': request.GET.get('restaurant_id', ''),
        #'table_id': request.GET.get('table_id', ''),      
        'number_of_seats': request.GET.get('number_of_seats', ''),
        'table_capacity': request.GET.get('table_capacity', ''),
        'table_number': request.GET.get('table_number', ''),
        'checkin': request.GET.get('checkin', ''),  # Get checkin date
        'checkintime': request.GET.get('checkintime', ''),  # Get checkin time
        'checkouttime': request.GET.get('checkouttime', ''),  # Get checkout time
    }


    if 'selection_data_objects' in request.session:
        selection_data = request.session['selection_data_objects']
        restaurant_id = str(request.GET.get('restaurant_id', ''))  # Use .get() to avoid KeyError

        if restaurant_id in selection_data:  
            # Ensure the keys exist before modifying them
            selection_data[restaurant_id]['checkintime'] = resturant_selection.get(restaurant_id, {}).get('checkintime', '')
            selection_data[restaurant_id]['checkouttime'] = resturant_selection.get(restaurant_id, {}).get('checkouttime', '')
        else:
            selection_data.update(resturant_selection)  # Add new room if not in session

        request.session['selection_data_objects'] = selection_data
        request.session.modified = True  # Force session update

    else:
        request.session['selection_data_objects'] = resturant_selection
        request.session.modified = True

    data = {
        'data': request.session['selection_data_objects'],
        "total_selected_item": len(request.session['selection_data_objects']),
    }

    return JsonResponse(data)




def remove_selection(request):
    hotel_id = str(request.GET['id'])
    if 'selection_data_object' in request.session:
        if hotel_id in request.session['selection_data_object']:
            selection_data = request.session['selection_data_object']
            del request.session['selection_data_object'][hotel_id]
            request.session['selection_data_object'] = selection_data

    total = 0
    room_count = 0
    total_days = 0
    checkin = ""
    checkout = ""
    hotel = None

    if 'selection_data_object' in request.session:
        for h_id, item in request.session['selection_data_object'].items():
                id = int(item['hotel_id'])
                checkin = item['checkin']
                checkout = item['checkout']
                room_type_ = int(item['room_type'])
                room_id = int(item['room_id'])

                user = request.user
                hotel = Hotel.objects.get(id=id)
                room_type = RoomType.objects.get(id=room_type_)
                room = Room.objects.get(id=room_id)

                new_date_format = "%Y-%m-%d"
                checkin_date = datetime.strptime(checkin, new_date_format)
                checkout_date = datetime.strptime(checkout, new_date_format)
                time_gap = checkout_date-checkin_date
                total_days = time_gap.days

                room_count += 1
                days = total_days
                price = room_type.price
                total_room_price = price * room_count
                total = total_room_price * days

        context = render_to_string(
            "hotel/async/rooms_selected.html",
                {
                    "data": request.session["selection_data_object"],
                    "total_selected_item": len(request.session["selection_data_object"]),
                    "total": total,
                    "total_days": total_days,
                    "checkin": checkin,
                    "checkout": checkout,
                    "hotel": hotel,
                },
            )
        print("context = ", context)
        return JsonResponse({"data" :context, "total_selected_item": len(request.session["selection_data_object"]),})

