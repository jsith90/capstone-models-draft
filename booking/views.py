from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages

def index(request):
    return render(request, "booking/index.html",{})

def table_booking(request):
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    days_open = valid_day(22)

    #Only show the days that are not full:
    validate_days = is_day_valid(days_open)
    

    if request.method == 'POST':
        seats = request.POST.get('seats')
        day = request.POST.get('day')
        if seats == None:
            messages.success(request, "Please Select Number of Seats!")
            return redirect('table_booking')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['seats'] = seats

        return redirect('table_booking_submit')


    return render(request, 'booking/table_booking.html', {
            'days_open':days_open,
            'validate_days':validate_days,
        })

def table_booking_submit(request):
    user = request.user
    times = [
        "1 PM", "3 PM", "5 PM", "7 PM", "9 PM"
    ]
    today = datetime.now()
    min_date = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    max_date = strdeltatime

    #Get stored data from django session:
    day = request.session.get('day')
    seats = request.session.get('seats')
    
    #Only show the time of the day that has not been selected before:
    # hour = check_time(times, day)
    available_times = check_time(times, day, seats)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = day_to_day_open(day)

        if seats != None:
            if day <= max_date and day >= min_date:
                if date == 'Thursday' or date == 'Friday' or date == 'Saturday' or date == 'Sunday':
                    if Table_Booking.objects.filter(day=day).count() < 40:
                        if time in available_times:
                        # if Table_Booking.objects.filter(day=day, time=time).count() < 1:
                            Table_Booking_Form = Table_Booking.objects.get_or_create(
                                user = user,
                                seats = seats,
                                day = day,
                                time = time,
                            )
                            messages.success(request, "Table Booking Made!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Already Been Taken!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select The Number of Seats!")
    if not available_times:
        messages.warning(request, "That booking is no longer available.")
        return render(request, 'booking/table_booking.html', {
            'days_open': days_open,
            'validate_days': validate_days,
        })

    return render(request, 'booking/table_booking_submit.html', {
        # 'times':hour,
        'times': available_times,
    })

def user_panel(request):
    user = request.user
    table_bookings = Table_Booking.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'user_panel.html', {
        'user':user,
        'table_bookings':table_bookings,
    })

def user_update(request, id):
    table_booking = Table_booking.objects.get(pk=id)
    user_date_selected = table_booking.day
    #Copy  booking:
    today = datetime.today()
    min_date = today.strftime('%Y-%m-%d')

    #24h if statement in template:
    delta24 = (user_date_selected).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    days_open = valid_days(22)

    #Only show the days that are not full:
    validate_days = is_day_valid(days_open)
    

    if request.method == 'POST':
        seats = request.POST.get('seats')
        day = request.POST.get('day')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['seats'] = seats

        return redirect('user_update_submit', id=id)


    return render(request, 'user_update.html', {
            'weekdays':weekdays,
            'validate_days':validate_days,
            'delta24': delta24,
            'id': id,
        })

def user_update_submit(request, id):
    user = request.user
    times = [
        "1 PM", "3 PM", "5 PM", "7 PM", "9 PM"
    ]
    today = datetime.now()
    min_date = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    max_date = strdeltatime

    day = request.session.get('day')
    seats = request.session.get('seats')
    
    #Only show the time of the day that has not been selected before and the time he is editing:
    hour = checkEditTime(times, day, id)
    table_booking = Table_booking.objects.get(pk=id)
    user_selected_time = appointment.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = day_to_day_open(day)

        if seats != None:
            if day <= max_date and day >= min_date:
                if date == 'Thursday' or date == 'Friday' or date == 'Saturday' or date == 'Sunday':
                    if Table_Booking.objects.filter(day=day).count() < 40:
                        if Table_Booking.objects.filter(day=day, time=time).count() < 1 or user_selected_time == time:
                            Table_Booking_Form = Table_Booking.objects.filter(pk=id).update(
                                user = user,
                                seats = seats,
                                day = day,
                                time = time,
                            ) 
                            messages.success(request, "Table Booking Edited!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Taken!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select Number of Seats!")
        return redirect('user_panel')


    return render(request, 'user_update_submit.html', {
        'times':hour,
        'id': id,
    })

def staff_panel(request):
    today = datetime.today()
    min_date = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    max_date = strdeltatime
    #Only show the Appointments 21 days from today
    items = Table_Bookings.objects.filter(day__range=[min_date, max_date]).order_by('day', 'time')

    return render(request, 'staff_panel.html', {
        'items':items,
    })

def day_to_day_open(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y

def valid_day(days):
    #Loop days you want in the next 21 days:
    today = datetime.now()
    valid_days = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Thursday' or y == 'Friday' or y == 'Saturday' or y == 'Sunday':
            valid_days.append(x.strftime('%Y-%m-%d'))
    return valid_days
    
def is_day_valid(x):
    validate_days = []
    for j in x:
        if Table_Booking.objects.filter(day=j).count() < 39:
            validate_days.append(j)
    return validate_days

# def check_time(times, day):
#     #Only show the time of the day that has not been selected before:
#     x = []
#     for k in times:
#         if Table_Booking.objects.filter(day=day, time=k).count() < 1:
#             x.append(k)
#     return x

def check_time(times, day, seats):
    # Get all bookings for the given day
    bookings = Table_Booking.objects.filter(day=day)
    
    # Initialize a list to store available times
    available_times = []
    
    # Iterate through each time slot
    for time in times:
        # Check if there's any booking for this time slot
        booking_exists = bookings.filter(time=time, seats=seats).exists()
        
        # If no booking exists, add the time slot to available times
        if not booking_exists:
            available_times.append(time)
    
    return available_times

def check_edit_time(times, day, id):
    #Only show the time of the day that has not been selected before:
    x = []
    table_booking = Table_Booking.objects.get(pk=id)
    time = table_booking.time
    for k in times:
        if Table_Booking.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x