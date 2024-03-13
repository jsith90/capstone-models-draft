from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    return render(request, "booking/index.html",{})

def table_booking(request):
    days_open = valid_day(22)
    validate_days = is_day_valid(days_open)
    if request.method == 'POST':
        table = request.POST.get('table')
        day = request.POST.get('day')
        if table == None:
            messages.success(request, "Please Select Your Table!")
            return redirect('table_booking')
        request.session['day'] = day
        request.session['table'] = table
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
    day = request.session.get('day')
    table = request.session.get('table')
    available_times = check_time(times, day, table)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = day_to_day_open(day)
        if table != None:
            if day <= max_date and day >= min_date:
                if date == 'Thursday' or date == 'Friday' or date == 'Saturday' or date == 'Sunday':
                    if Table_Booking.objects.filter(day=day).count() < 40:
                        if time in available_times:
                            Table_Booking_Form = Table_Booking.objects.get_or_create(
                                user = user,
                                table = table,
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
            messages.success(request, "Please Select Your Table!")
    if not available_times:
        messages.warning(request, "That booking is no longer available.")
        days_open = valid_day(22)
        validate_days = is_day_valid(days_open)
        return render(request, 'booking/table_booking.html', {
            'days_open': days_open,
            'validate_days': validate_days,
        })
    return render(request, 'booking/table_booking_submit.html', {
        'times': available_times,
    })

@login_required
def user_panel(request):
    user = request.user
    current_date = datetime.now().date()
    table_bookings = Table_Booking.objects.filter(user=user, day__gte=current_date).order_by('day', 'time')
    today = date.today() 
    return render(request, 'booking/user_panel.html', {
        'user':user,
        'table_bookings':table_bookings,
        'today': today,
    })

def user_update(request, id):
    table_booking = Table_Booking.objects.get(pk=id)
    user_date_selected = table_booking.day
    today = datetime.today()
    min_date = today.strftime('%Y-%m-%d')
    delta24 = (user_date_selected).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    days_open = valid_day(22)
    validate_days = is_day_valid(days_open)
    if request.user == table_booking.user:
        if   request.method == 'POST':
            table = request.POST.get('table')
            day = request.POST.get('day')
            request.session['day'] = day
            request.session['table'] = table
            return redirect('user_update_submit', id=id)
    else:
        messages.success(request, "Unauthorised access.")
        return render(request, 'booking/index.html')
    return render(request, 'booking/user_update.html', {
            'days_open':days_open,
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
    table = request.session.get('table')
    hour = check_edit_time(times, day, id)
    table_booking = Table_Booking.objects.get(pk=id)
    user_selected_time = table_booking.time
    if user == table_booking.user:
        if request.method == 'POST':
            time = request.POST.get("time")
            date = day_to_day_open(day)
            if table != None:
                if day <= max_date and day >= min_date:
                    if date == 'Thursday' or date == 'Friday' or date == 'Saturday' or date == 'Sunday':
                        if Table_Booking.objects.filter(day=day).count() < 40:
                            if Table_Booking.objects.filter(day=day, time=time).count() < 1 or user_selected_time == time:
                                Table_Booking_Form = Table_Booking.objects.filter(pk=id).update(
                                    user = user,
                                    table = table,
                                    day = day,
                                    time = time,
                                ) 
                                messages.success(request, "Your Booking Has Been Successfully Updated!")
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
                messages.success(request, "Please Select Your Table!")
            return redirect('user_panel')
        return render(request, 'booking/user_update_submit.html', {
        'times':hour,
        'id': id,
        })
    else:
        return render(request, 'booking/index.html')
        
def staff_panel(request):
    today = datetime.today()
    min_date = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    max_date = strdeltatime
    items = Table_Booking.objects.filter(day__range=[min_date, max_date]).order_by('day', 'time')
    return render(request, 'booking/staff_panel.html', {
        'items':items,
    })

def day_to_day_open(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y

def valid_day(days):
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

def check_time(times, day, table):
    bookings = Table_Booking.objects.filter(day=day)
    available_times = []
    for time in times:
        booking_exists = bookings.filter(time=time, table=table).exists()
        if not booking_exists:
            available_times.append(time)
    return available_times

def check_edit_time(times, day, id):
    x = []
    table_booking = Table_Booking.objects.get(pk=id)
    time = table_booking.time
    for k in times:
        if Table_Booking.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x

def delete_booking(request, booking_id):
    table_booking = Table_Booking.objects.get(pk=booking_id)
    if request.user.is_authenticated:
        today = datetime.today()
        booking_date = table_booking.day
        min_deletion_date = today + timedelta(days=1)
        if booking_date >= min_deletion_date.date():
            table_booking.delete()
            messages.success(request, ("Booking successfully cancelled!"))
            return redirect ('user_panel')
        else:
            messages.success(request, "You cannot delete this booking as it is less than 24 hours ahead of the booking time.")
    else:
        messages.success(request, ("You aren't authorised to do that!"))
        return redirect('user_panel')