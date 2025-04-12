from django.shortcuts import render, redirect
from hotel.models import Hotel, HotelGallery, HotelFeatures, HotelFaqs, RoomType, Room, Booking, ActivityLog, StaffOnDuty, Coupon, Resturant, ResturantBooking
from django.contrib import messages
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from hotel.forms import HotelForm, RoomTypeForm, RoomForm, ResturantForm, CouponForm
from django.contrib.auth.decorators import login_required

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
    if request.method == "POST":
        code = request.POST.get("code")
        try:
            coupon = Coupon.objects.get(code__iexact=code, active = True)
            if coupon in booking.coupons.all():
                messages.warning(request, "Coupon already in used")
                return redirect("hotel:checkout", booking.booking_id)
            else:
                if coupon.type == "Percentage":
                    discount = booking.total * coupon.discount / 100 # Calculating the total discount amount that will be given of the coupon
                else:
                    discount = coupon.discount
                booking.coupons.add(coupon)
                booking.total -= discount
                booking.saved_amount += discount
                booking.save() 

                messages.success(request, "Coupon activated")
                return redirect("hotel:checkout", booking.booking_id)
        except:
            messages.error(request, "Coupon is not available")
            return redirect("hotel:checkout", booking.booking_id)
    context = {
        "booking": booking
    }
    return render(request, "hotel/checkout.html", context)

def resturant(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    context = {
        "hotel": hotel,
    }
    return render(request, "hotel/resturant_detail.html", context)


def resturant_detail(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    #resturant = get_object_or_404(Resturant, hotel=hotel, is_available=True)
    resturant = Resturant.objects.filter(hotel=hotel)
    
    context = {
        "hotel": hotel,
        "resturant": resturant,
    }
    return render(request, "hotel/resturant_detail.html", context)


def resturant_table_detail(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    resturant = Resturant.objects.filter(hotel=hotel, is_available = True)
    id = request.GET.get("hotel-id")
    checkin = request.GET.get("checkin")
    
    checkintime = request.GET.get("checkintime")
    checkouttime = request.GET.get("checkouttime")

    context = {
        "hotel": hotel,
        "resturant": resturant,
        "checkin": checkin,
        
        "checkintime": checkintime,
        "checkouttime": checkouttime,
    }
    return render(request, "hotel/resturant_table_detail.html", context)


def restaurant_selected(request):
    total_time = 0  # Total time in hours
    table_count = 0
    checkin = ""
    checkintime = ""
    checkouttime = ""

    if 'selection_data_objects' in request.session:
        if request.method == "POST":
            for r_id, item in request.session['selection_data_objects'].items():
                id = int(item['hotel_id'])
                checkin = item['checkin']
                checkintime = item.get('checkintime', '00:00')
                checkouttime = item.get('checkouttime', '00:00')
                restaurant_id = int(item['restaurant_id'])

                user = request.user
                hotel = Hotel.objects.get(id=id)
                restaurant = Resturant.objects.get(id=restaurant_id)

                # Calculate total time in hours
                time_format = "%H:%M"
                checkin_time_obj = datetime.strptime(checkintime, time_format)
                checkout_time_obj = datetime.strptime(checkouttime, time_format)
                time_gap = checkout_time_obj - checkin_time_obj
                total_time = time_gap.total_seconds() / 3600  # Convert to hours

                full_name = request.POST.get('full_name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')

                booking = ResturantBooking.objects.create(
                    hotel=hotel,
                    resturant=restaurant,
                    check_in_date=checkin,
                    check_in_time=checkintime,
                    check_out_time=checkouttime,
                    total_time=total_time,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    user=request.user if request.user.is_authenticated else None
                )

                for r_id, item in request.session['selection_data_objects'].items():
                    restaurant_id = item['restaurant_id']
                    restaurant = Resturant.objects.get(id=restaurant_id)
                    
                    table_count += 1

                booking.save()
                return redirect("hotel:restaurant_checkout", booking.rbooking_id)

        hotel = None
        for r_id, item in request.session['selection_data_objects'].items():
            id = int(item['hotel_id'])
            checkin = item['checkin']
            checkintime = item.get('checkintime') or '00:00'
            checkouttime = item.get('checkouttime') or '00:00'      
            restaurant_id_ = item.get('restaurant_id')

            # Calculate total time in hours
            time_format = "%H:%M"
            checkin_time_obj = datetime.strptime(checkintime, time_format)
            checkout_time_obj = datetime.strptime(checkouttime, time_format)
            time_gap = checkout_time_obj - checkin_time_obj
            total_time = time_gap.total_seconds() / 3600

            hotel = Hotel.objects.get(id=id)
            table_count += 1

        context = {
            "resturantdata": request.session['selection_data_objects'],
            "total_selected_items": len(request.session['selection_data_objects']),
            "total_time": total_time,
            "hotel": hotel,
            "checkin": checkin,
            "checkintime": checkintime,
            "checkouttime": checkouttime,
        }
        return render(request, "hotel/restaurant_selected.html", context)

    else:
        messages.warning(request, "No restaurants selected")
        return redirect("/")

def restaurant_checkout(request, booking_id):
    booking = ResturantBooking.objects.get(rbooking_id=booking_id)

    context = {
        "booking": booking
    }

    return render(request, "hotel/resturant_checkout.html", context)
    

def add_hotels(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in before adding hotel.")
        return redirect("userauthentication:sign-in")  
        
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save()
            hotel.owner = request.user
            hotel.save()
            return redirect("/")
    else:
        form = HotelForm()
    return render(request, 'hotel/add_hotel.html', {'form': form})


def add_room_types(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in before adding room types.")
        return redirect("userauthentication:sign-in")
        
    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            room_type = form.save(commit=False)
            
            if not request.user.is_superuser:
                # If not superuser, it allows to add roomtype to their own hotel
                hotel = form.cleaned_data['hotel']
                if hotel.owner != request.user:
                    return redirect('unauthorized')  
            
            room_type.save()
            return redirect("/")  # Redirect after saving
    else:
        form = RoomTypeForm()
        
        # Optional: Filter hotel dropdown to show only user's hotels
        #if not request.user.is_superuser:
        #    form.fields['hotel'].queryset = Hotel.objects.filter(owner=request.user)
    
    return render(request, 'hotel/add_room_type.html', {'form': form})


def add_rooms(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in before adding rooms.")
        return redirect("userauthentication:sign-in")
        
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            
            if not request.user.is_superuser:
                hotel = form.cleaned_data['hotel']
                if hotel.owner != request.user:
                    return redirect('unauthorized')  # Redirect to an unauthorized page or message
            
            room.save()  # Save the room after validation
            return redirect("/")  # Redirect to another page after saving
    else:
        form = RoomForm()
    
    return render(request, 'hotel/add_room.html', {'form': form})


def add_restaurants(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in before adding restaurant.")
        return redirect("userauthentication:sign-in")
            
    if request.method == 'POST':
        form = ResturantForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if user is the owner of the selected hotel
            hotel = form.cleaned_data['hotel']
            if hotel.owner != request.user:
                messages.error(request, "You can only add restaurants to hotels you own.")
                return redirect("/")
                
            restaurant = form.save()
            messages.success(request, "Restaurant table added successfully!")
            return redirect("/")
    else:
        # Only show hotels owned by the current user
        form = ResturantForm()
        if request.user.is_authenticated:
            form.fields['hotel'].queryset = Hotel.objects.filter(owner=request.user)
    
    return render(request, 'hotel/add_restaurant.html', {'form': form})

def add_coupons(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in before adding a coupon.")
        return redirect("userauthentication:hotel-sign-in")

    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            # Check if user is the owner of the selected hotel
            hotel = form.cleaned_data['hotel']
            if hotel and hotel.owner != request.user and not request.user.is_superuser:
                messages.error(request, "You can only add coupons to hotels you own.")
                return redirect("/")

            coupon = form.save()
            messages.success(request, f"Coupon {coupon.code} added successfully!")
            return redirect("/")
    else:
        form = CouponForm()
        if request.user.is_authenticated and not request.user.is_superuser:
            form.fields['hotel'].queryset = Hotel.objects.filter(owner=request.user)

    return render(request, 'hotel/add_coupon.html', {'form': form})
