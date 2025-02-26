from django.shortcuts import render, redirect
from hotel.models import Hotel, HotelGallery, HotelFeatures, HotelFaqs, RoomType, Room, Booking, ActivityLog, StaffOnDuty
from django.contrib import messages
from datetime import datetime

def index (request):
    hotels = Hotel.objects.filter(status="Live")
    context = {
        "hotels" : hotels
    }
    return render(request, "hotel/hotel.html", context)


def hotel_detail(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    context = {
        "hotel": hotel,
    }
    return render(request, "hotel/hotel_detail.html", context)


def room_type_detail(request, slug, roomtype_slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    room_type = RoomType.objects.get(hotel=hotel, slug=roomtype_slug)
    rooms = Room.objects.filter(room_type=room_type, is_available = True)

    id = request.GET.get("hotel-id")
    checkin = request.GET.get("checkin")
    checkout = request.GET.get("checkout")

    context = {
        "hotel": hotel,
        "room_type": room_type,
        "rooms": rooms,
        "checkin": checkin,
        "checkout": checkout,
    }
    return render(request, "hotel/room_type_detail.html", context)

def rooms_selected(request):
    total = 0
    room_count = 0
    total_days = 0
    checkin = ""
    checkout = ""

    if 'selection_data_object' in request.session:

        if request.method == "POST":
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

            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            booking = Booking.objects.create(
                hotel=hotel,
                room_type=room_type,
                check_in_date=checkin,
                check_out_date=checkout,
                total_days=total_days,
                full_name=full_name,
                email=email,
                phone=phone
            )

            if request.user.is_authenticated:
                booking.user = request.user
                booking.save()
            else:
                booking.user == None
                booking.save()

            for h_id, item in request.session['selection_data_object'].items():
                room_id = int(item['room_id']) 
                room = Room.objects.get(id=room_id)
                booking.room.add(room)

                room_count  += 1
                days = total_days
                price = room_type.price
                total_room_price = price * room_count
                total = total_room_price * days
            booking.total += float(total)
            booking.before_discount += float(total)
            booking.save()
            return redirect("hotel:checkout", booking.booking_id)

        hotel = None
        for h_id, item in request.session['selection_data_object'].items():
            id = int(item['hotel_id'])
            checkin = item['checkin']
            checkout = item['checkout']
            room_type_ = int(item['room_type'])
            room_id = int(item['room_id'])

            room_type = RoomType.objects.get(id=room_type_)


            new_date_format = "%Y-%m-%d"
            checkin_date = datetime.strptime(checkin, new_date_format)
            checkout_date = datetime.strptime(checkout, new_date_format)
            time_gap = checkout_date-checkin_date
            total_days = time_gap.days

            room_count  += 1
            days = total_days
            price = room_type.price
            total_room_price = price * room_count
            total = total_room_price * days
            hotel = Hotel.objects.get(id=id)
        context = {
            "data": request.session['selection_data_object'],
            "total_selected_items": len(request.session['selection_data_object']),
            "total": total,
            "total_days": total_days,
            "hotel": hotel,
            "checkin": checkin,
            "checkout": checkout,
            "total": total,

        }
        return render(request, "hotel/rooms_selected.html", context)

    else:
        messages.warning(request, "No rooms Selected")
        return redirect("/")
    
def checkout(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)

    context = {
        "booking": booking
    }
    return render(request, "hotel/checkout.html", context)
