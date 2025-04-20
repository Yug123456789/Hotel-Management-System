from django.shortcuts import render, redirect
from hotel.models import Hotel, HotelGallery,   RoomType, Room, Booking, ActivityLog, StaffOnDuty, Coupon, Resturant, ResturantBooking, Bookmark, Payment
from django.contrib import messages
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from hotel.forms import HotelForm, RoomTypeForm, RoomForm, ResturantForm, CouponForm
import uuid, hmac, hashlib
from django.utils import timezone
import requests, json
from django.db.models import Q




def index (request):
    hotels = Hotel.objects.filter(status="Live")
    bookmarked_ids = []

    if request.user.is_authenticated:
        bookmarked_ids = Bookmark.objects.filter(user=request.user).values_list('hotel_id', flat=True)
    context = {
        "hotels" : hotels,
        'bookmarked_ids': bookmarked_ids,
    }
    return render(request, "hotel/hotel.html", context)


def hotel_detail(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    context = {
        "hotel": hotel,
    }
    return render(request, "hotel/hotel_detail.html", context)


def hotel_user_hotel_detail(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    context = {
        "hotel": hotel,
    }
    return render(request, "user_hotel/hotel_user_hotel_detail.html", context)

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

def hotel_user_room_type_detail(request, slug, roomtype_slug):
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
    return render(request, "user_hotel/hotel_user_room_type_detail.html", context)

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
                phone=phone,
                is_active=True
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
                room.is_available = False
                room.save()

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
    booking = get_object_or_404(Booking, booking_id=booking_id)

    purchase_order_id = str(uuid.uuid4())
    # Handle coupon logic
    if request.method == "POST":
        code = request.POST.get("code")
        
        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            if coupon in booking.coupons.all():
                messages.warning(request, "Coupon already in use")
            else:
                discount = booking.total * coupon.discount / 100 if coupon.type == "Percentage" else coupon.discount
                booking.coupons.add(coupon)
                booking.total -= discount
                booking.saved_amount += discount
                
                booking.save()
                messages.success(request, "Coupon activated")
        except:
            messages.error(request, "Coupon is not available")
        return redirect("hotel:checkout", booking.booking_id)  

    context = {
    "booking": booking,
    "uuid": purchase_order_id,
    
    }

    return render(request, "hotel/checkout.html", context)

def initiatekhalti(request):
    url = "https://dev.khalti.com/api/v2/epayment/initiate/"
    return_url = request.POST.get('return_url')
    purchase_order_id = request.POST.get('purchase_order_id')
    booking_id = request.POST.get('booking_id')  # Get the booking_id from the form

    amount = int(float(request.POST.get('amount')) * 100)
    full_name = request.POST.get('full_name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')

    # Store the purchase_order_id in the booking
    booking = Booking.objects.get(booking_id=booking_id)
    booking.khalti_payment = purchase_order_id
    booking.save()
    
    print("return_url", return_url)
    print("purchase_order_id", purchase_order_id)
    
    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
            "name": full_name,
            "email": email,
            "phone": phone
        }
    })
    headers = {
        'Authorization': 'key 88f7db09b44d4da794fed1e886e24bb9',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    new_res = json.loads(response.text)
    print(new_res)
    return redirect(new_res['payment_url'])


def khalti_payment_verify(request):
    pidx = request.GET.get('pidx')
    transaction_id = request.GET.get('transaction_id')
    status = request.GET.get('status')
    purchase_order_id = request.GET.get('purchase_order_id')
    total_amount = request.GET.get('total_amount')
    
    print(f"Payment data received: pidx={pidx}, status={status}, purchase_order_id={purchase_order_id}")
    
    if status == 'Completed':
        try:
            # Find the booking using the purchase_order_id we stored
            booking = Booking.objects.get(khalti_payment=purchase_order_id)
            
            # Update booking payment status
            booking.payment_status = 'paid'
            booking.save()
            
            # Create payment record
            payment = Payment.objects.create(
                booking=booking,
                amount=float(total_amount) / 100 if total_amount else booking.total,
                transaction_id=transaction_id or pidx,
                payment_method='Khalti',
                status='paid'
            )
            
            messages.success(request, "Payment successful!")
            return redirect('hotel:customer_user_room_booking')
        
        except Booking.DoesNotExist:
            messages.error(request, "Could not locate your booking. Please contact support.")
            return redirect('hotel:index')
        except Exception as e:
            print(f"Error processing payment: {str(e)}")
            messages.error(request, f"Payment verification failed: {str(e)}")
            return redirect('hotel:index')
    else:
        messages.error(request, "Payment failed or incomplete. Please try again.")
        return redirect('hotel:index')
    
# This views is to display the payment details from 
# payment models for hotel user of the logged in user     
def payment_details(request):
    if request.user.is_authenticated:
        payments = Payment.objects.filter(booking__user=request.user)
        return render(request, 'user_hotel/payment_details.html', {'payments': payments})
    else:
        # Redirect to login or show error
        return redirect('login')    

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

def hotel_user_resturant(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    #resturant = get_object_or_404(Resturant, hotel=hotel, is_available=True)
    resturant = Resturant.objects.filter(hotel=hotel)
    
    context = {
        "hotel": hotel,
        
    }
    return render(request, "user_hotel/hotel_user_resturant_detail.html", context)


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

def hotel_user_resturant_table_detail(request, slug):
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
    return render(request, "user_hotel/hotel_user_resturant_table_detail.html", context)



def restaurant_selected(request):
    total_time = 0
    table_count = 0
    checkin = ""
    checkintime = ""
    checkouttime = ""

    if 'selection_data_objects' in request.session:
        if request.method == "POST":
            table_numbers_list = []  #  Collect selected table numbers

            for r_id, item in request.session['selection_data_objects'].items():
                hotel_id = int(item['hotel_id'])
                checkin = item['checkin']
                checkintime = item.get('checkintime', '00:00')
                checkouttime = item.get('checkouttime', '00:00')
                restaurant_id = int(item['restaurant_id'])
                table_number = item.get('table_number')  #  Get table number

                # Parse time and calculate duration
                time_format = "%H:%M"
                checkin_time_obj = datetime.strptime(checkintime, time_format)
                checkout_time_obj = datetime.strptime(checkouttime, time_format)
                time_gap = checkout_time_obj - checkin_time_obj
                total_time = time_gap.total_seconds() / 3600

                if table_number:
                    table_numbers_list.append(table_number)

                # Get form data
                full_name = request.POST.get('full_name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')

                hotel = Hotel.objects.get(id=hotel_id)

                # Create the booking
                booking = ResturantBooking.objects.create(
                    hotel=hotel,
                    check_in_date=checkin,
                    check_in_time=checkintime,
                    check_out_time=checkouttime,
                    total_time=total_time,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    user=request.user if request.user.is_authenticated else None,
                    table_numbers=", ".join(table_numbers_list)  #  Save table numbers
                )

                # Adds all selected tables to booking
                for r_id, item in request.session['selection_data_objects'].items():
                    restaurant_table_id = item['restaurant_id']
                    table = Resturant.objects.get(id=restaurant_table_id)
                    booking.tables.add(table)
                    table_count += 1

                booking.save()

                return redirect("hotel:restaurant_checkout", booking.rbooking_id)

        # If GET request — just display the current selection summary
        hotel = None
        for r_id, item in request.session['selection_data_objects'].items():
            hotel_id = int(item['hotel_id'])
            checkin = item['checkin']
            checkintime = item.get('checkintime') or '00:00'
            checkouttime = item.get('checkouttime') or '00:00'

            # Calculate total time
            time_format = "%H:%M"
            checkin_time_obj = datetime.strptime(checkintime, time_format)
            checkout_time_obj = datetime.strptime(checkouttime, time_format)
            time_gap = checkout_time_obj - checkin_time_obj
            total_time = time_gap.total_seconds() / 3600

            hotel = Hotel.objects.get(id=hotel_id)
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
        return redirect("userauthentication:hotel-sign-in")  
        
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save()
            hotel.owner = request.user
            hotel.save()
            return redirect("hotel:user_hotel")
    else:
        form = HotelForm()
    return render(request, 'hotel/add_hotel.html', {'form': form})


def edit_hotel_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in before editing hotel.")
        return redirect("userauthentication:hotel-sign-in")  
    
    user_hotels = Hotel.objects.filter(owner=request.user)
    return render(request, 'hotel/edit_hotel_list.html', {'hotels': user_hotels})


def edit_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)

    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotel updated successfully.")
            return redirect('hotel:edit_hotel_list')
    else:
        form = HotelForm(instance=hotel)

    return render(request, 'hotel/edit_hotel.html', {'form': form})


def add_room_types(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in before adding room types.")
        return redirect("userauthentication:hotel-sign-in")

    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        
        #  Set the hotel queryset
        hotels = Hotel.objects.filter(owner=request.user)
        form.fields['hotel'].queryset = hotels

        # If there's only one hotel, pre-fill it
        if hotels.count() == 1:
            form.fields['hotel'].initial = hotels.first()

        if form.is_valid():
            room_type = form.save(commit=False)

            if not request.user.is_superuser:
                hotel = form.cleaned_data['hotel']
                if hotel.owner != request.user:
                    return redirect('unauthorized')

            room_type.save()
            return redirect("hotel:user_hotel")
    else:
        form = RoomTypeForm()
        
        #  Set the hotel queryset
        hotels = Hotel.objects.filter(owner=request.user)
        form.fields['hotel'].queryset = hotels

        #  If there's only one hotel, pre-fill it
        if hotels.count() == 1:
            form.fields['hotel'].initial = hotels.first()

    return render(request, 'hotel/add_room_type.html', {'form': form})



def user_room_types(request):
    # Fetch all room types where the hotel belongs to the current user
    room_types = RoomType.objects.filter(hotel__owner=request.user)
    return render(request, 'hotel/user_room_types.html', {'room_types': room_types})

def edit_room_type(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id, hotel__owner=request.user)

    if request.method == 'POST':
        form = RoomTypeForm(request.POST, instance=room_type)
        if form.is_valid():
            form.save()
            messages.success(request, "Room Type updated successfully.")
            return redirect('hotel:user_room_types')
    else:
        form = RoomTypeForm(instance=room_type)

    form.fields['hotel'].queryset = Hotel.objects.filter(owner=request.user)
    return render(request, 'hotel/edit_room_type.html', {'form': form})


def add_rooms(request):
    if not request.user.is_authenticated:  # Make sure user is logged in
        messages.warning(request, "You have to log in before adding rooms.")
        return redirect("userauthentication:hotel-sign-in")

    if request.method == 'POST':  # If form is submitted (If the request method is post method)
        form = RoomForm(request.POST, user=request.user)  # Pass the user to the form

        hotels = Hotel.objects.filter(owner=request.user)  # Only show hotels the user owns
        form.fields['hotel'].queryset = hotels  # Set those hotels in the dropdown
        if hotels.count() == 1:
            form.fields['hotel'].initial = hotels.first()  #  This auto-selects the hotel if there's only one

        room_types = RoomType.objects.filter(hotel__owner=request.user)  # Get room types from user's hotels
        form.fields['room_type'].queryset = room_types  # Set them in the dropdown
        if room_types.count() == 1:
            form.fields['room_type'].initial = room_types.first()  #  This auto-selects room type if only one exists

        if form.is_valid():  # If all form data is valid
            room = form.save(commit=False)  # Create room object but don’t save to DB yet

            if not request.user.is_superuser:  # Extra check: if not admin
                hotel = form.cleaned_data['hotel']  # Get selected hotel
                if hotel.owner != request.user:  # If it's not the user's hotel, block it
                    return redirect('unauthorized')

            room.save()  # Save the room to Database
            return redirect("hotel:user_hotel")  # Redirect the user to user_hotel page after saving

    else:  
        form = RoomForm(user=request.user)  # Create empty form for the user

        hotels = Hotel.objects.filter(owner=request.user)  # Filter hotels by owner
        form.fields['hotel'].queryset = hotels  # Set filtered hotels in dropdown
        if hotels.count() == 1:
            form.fields['hotel'].initial = hotels.first()  #  Pre-select the hotel if there's only one

        room_types = RoomType.objects.filter(hotel__owner=request.user)  
        form.fields['room_type'].queryset = room_types
        if room_types.count() == 1:
            form.fields['room_type'].initial = room_types.first()  #  Pre-select room type if only one exists

    return render(request, 'hotel/add_room.html', {'form': form})  # Show the form on the page




def user_rooms(request):
    rooms = Room.objects.filter(hotel__owner=request.user)
    return render(request, 'hotel/user_rooms.html', {'rooms': rooms})

def edit_room(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "You must log in first.")
        return redirect("userauthentication:hotel-sign-in")

    room = get_object_or_404(Room, pk=pk)

    # Ensure the user is the owner
    if not request.user.is_superuser and room.hotel.owner != request.user:
        return redirect('unauthorized')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("hotel:user_hotel")
    else:
        form = RoomForm(instance=room)
        form.fields['hotel'].queryset = Hotel.objects.filter(owner=request.user)

    return render(request, 'hotel/edit_room.html', {'form': form})


def add_restaurants(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in before adding restaurant.")
        return redirect("userauthentication:hotel-sign-in")
            
    if request.method == 'POST':
        form = ResturantForm(request.POST, request.FILES)

        hotels = Hotel.objects.filter(owner=request.user)
        form.fields['hotel'].queryset = hotels          #filtering the hotel on dropdown according to the user
        if hotels.count() == 1:
            form.fields['hotel'].initial = hotels.first()   # Auto selecting the first hotel in ndropdown instead of showing ----

        if form.is_valid():
            hotel = form.cleaned_data['hotel']
            if hotel.owner != request.user:
                messages.error(request, "You can only add restaurants to hotels you own.")
                return redirect("/")

            form.save()
            messages.success(request, "Restaurant table added successfully!")
            return redirect("hotel:user_hotel")

    else:
        form = ResturantForm()

        hotels = Hotel.objects.filter(owner=request.user)
        form.fields['hotel'].queryset = hotels    #filtering the hotel on dropdown
        if hotels.count() == 1:
            form.fields['hotel'].initial = hotels.first()   # Auto selecting the first hotel in ndropdown instead of showing ----

    return render(request, 'hotel/add_restaurant.html', {'form': form})


def user_restaurants(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must log in to view your restaurant tables.")
        return redirect("userauthentication:hotel-sign-in")

    restaurants = Resturant.objects.filter(hotel__owner=request.user)
    return render(request, 'hotel/user_restaurants.html', {'restaurants': restaurants})

def edit_restaurant(request, pk):
    restaurant = get_object_or_404(Resturant, pk=pk)

    if restaurant.hotel.owner != request.user:
        return redirect('unauthorized')

    if request.method == 'POST':
        form = ResturantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, "Restaurant table updated successfully.")
            return redirect("hotel:user_restaurants")
    else:
        form = ResturantForm(instance=restaurant)
        form.fields['hotel'].queryset = Hotel.objects.filter(owner=request.user)

    return render(request, 'hotel/edit_restaurant.html', {'form': form})

def add_coupons(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in before adding a coupon.")
        return redirect("userauthentication:hotel-sign-in")

    if request.method == 'POST':
        form = CouponForm(request.POST, user=request.user)  
        if form.is_valid():
            hotel = form.cleaned_data['hotel']
            if hotel and hotel.owner != request.user and not request.user.is_superuser:
                messages.error(request, "You can only add coupons to hotels you own.")
                return redirect("/")
            coupon = form.save()
            messages.success(request, f"Coupon {coupon.code} added successfully!")
            return redirect("hotel:user_hotel")
    else:
        form = CouponForm(user=request.user)  
        
        # Filter hotels owned by the logged-in user to show in the dropdown
        if request.user.is_authenticated:
            form.fields['hotel'].queryset = Hotel.objects.filter(owner=request.user)
            
        # Auto-select if there is only one hotel owned by the user
        hotels = Hotel.objects.filter(owner=request.user)
        if hotels.count() == 1:
            form.fields['hotel'].initial = hotels.first()  # Select the first hotel if there's only one

    return render(request, 'hotel/add_coupon.html', {'form': form})




def user_hotel(request):
    hotels = Hotel.objects.filter(status="Live")
    context = {
        "hotels" : hotels
    }
    return render(request, 'user_hotel/hotel_user.html', context)

# Displays the Room booking sectio of hotel user.
def user_hotel_dashboard(request):
    hotel_id = request.GET.get('hotel_id')

    
    bookings = Booking.objects.filter(user=request.user)

    
    if hotel_id:
        bookings = bookings.filter(hotel__id=hotel_id)

    
    hotels = Hotel.objects.filter(booking__user=request.user).distinct()

    context = {
        'booking': bookings,
        'selected_hotel_id': hotel_id,
        'hotels': hotels,  
    }
    return render(request, 'hotel/hotel_user_dashboard.html', context)



def user_hotel_restaurant_booking(request):
    hotel_id = request.GET.get('hotel_id')
    
    # Get restaurant bookings for the logged-in user
    booking = ResturantBooking.objects.filter(user=request.user)

    # Filter by selected hotel 
    if hotel_id:
        booking = booking.filter(hotel__id=hotel_id)

    # Get only hotels the user has restaurant bookings 
    hotels = Hotel.objects.filter(resturantbooking__user=request.user).distinct()

    context = {
        'booking': booking,
        'selected_hotel_id': hotel_id,
        'hotels': hotels,
    }
    return render(request, 'hotel/hotel_user_restaurant_booking.html', context)



def user_customer_room_booking(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in first.")
        return redirect('userauthentication:sign-in')
    
    hotel_id = request.GET.get('hotel_id')

    booking = Booking.objects.filter(user=request.user)

    context = {
        'booking': booking,
        'selected_hotel_id': hotel_id,
        'hotels': Hotel.objects.all(),
    }
    return render(request, 'hotel/customer_room_booking.html', context)

def user_customer_table_booking(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in first.")
        return redirect('userauthentication:sign-in')

    bookings = ResturantBooking.objects.filter(user=request.user).order_by('-check_in_date')

    context = {
        'table_bookings': bookings
    }
    return render(request, 'hotel/customer_table_booking.html', context)

def bookmark_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, hotel=hotel)
    if not created:
        bookmark.delete()  
    return redirect('hotel:index')


def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'hotel/my_bookmarks.html', {'bookmarks': bookmarks})



def update_room_status(request):
    today = timezone.now().date()
    
    # Get all active bookings
    active_bookings = Booking.objects.filter(is_active=True)
    
    # Keep track of which rooms should be unavailable
    unavailable_room_ids = set()
    
    # For active bookings that are current (today is between check-in and check-out)
    for booking in active_bookings:
        if booking.check_in_date <= today <= booking.check_out_date:
            # Add room IDs to our set
            room_ids = booking.room.values_list('id', flat=True)
            unavailable_room_ids.update(room_ids)
    
    # Mark rooms in active bookings as unavailable
    if unavailable_room_ids:
        Room.objects.filter(id__in=unavailable_room_ids).update(is_available=False)
    
    # Mark rooms not in active bookings as available
    Room.objects.exclude(id__in=unavailable_room_ids).update(is_available=True)
    
    return redirect('hotel:user_hotel')