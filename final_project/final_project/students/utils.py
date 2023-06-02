from django.shortcuts import redirect
from datetime import datetime, time, timedelta
from final_project.dininghall.models import table_time, table_menu, table_booking_dininghall
from django.contrib import messages

def create_booking(student, menu, vacancy, time_suggested):
    booking = table_booking_dininghall.objects.create(
        students_nim=student,
        available=vacancy,
        time_booked=time_suggested,
        menu=menu
    )
    menu.available = vacancy
    menu.save()
    return booking

def get_latest_booking_for_menu(menu):
    latest_booking_for_menu = table_booking_dininghall.objects.filter(menu=menu).latest('id')
    return latest_booking_for_menu

def get_latest_booking(user):
    latest_booking = table_booking_dininghall.objects.filter(students_nim=user).latest('created_at')
    return latest_booking

def is_within_restricted_range(booked_suggestion_time, current_hour):
    return (
        (time(7, 0, 0) <= booked_suggestion_time <= time(8, 59, 59) and current_hour < time(9, 0, 0) or current_hour > time(19, 0, 0))
        or (time(11, 0, 0) <= booked_suggestion_time <= time(13, 59, 59) and current_hour < time(14, 0, 0))
        or (time(17, 0, 0) <= booked_suggestion_time <= time(18, 59, 59) and current_hour < time(19, 0, 0))
    )

def get_student_dininghall_context(request):
    current_hour, current_date = get_current_hour_and_current_date()
    session, time_objects = get_session_and_time_objects(current_hour)
    menu_object = table_menu.objects.filter(date=current_date, session=session).first()
    suggestion_time = get_suggestion_time().strftime('%H:%M:%S')
    has_booked = table_booking_dininghall.objects.filter(students_nim=request.user).exists()

    if has_booked:
        latest_booking = get_latest_booking(request.user)
        booked_suggestion_time = latest_booking.time_booked
        menu = latest_booking.menu
        booked_menu = menu.menu
        booked_session = menu.session

        if is_within_restricted_range(booked_suggestion_time, current_hour):
            context = {
                'session': booked_session,
                'menu_object': booked_menu,
                'time_suggested': booked_suggestion_time.strftime('%H:%M:%S'),
                'has_booked': has_booked,
                'day': current_date.strftime('%A'),
            }
            return context

    context = {
        'time_objects': time_objects,
        'menu_object': menu_object,
        'time_suggested': suggestion_time,
        'session': session,
        'date': current_date,
        'day': current_date.strftime('%A'),
        'has_booked': has_booked,
    }
    return context

def get_menu_based_date_and_session(date, session):
    menu = table_menu.objects.filter(date=date, session=session).first()
    return menu

def not_student(request):
    messages.error(request, 'You are not authorized to access student resources. You need the Student role.')
    return redirect('dininghall_index')

def get_current_hour_and_current_date():
    current_hour = datetime.now().time()
    current_date = datetime.now().date()
    if time(20, 0) <= current_hour <= time(23, 59, 59):
        current_date += timedelta(days=1)
    return current_hour, current_date

def get_suggestion_time():
    suggestion_time = time(8,0,0)
    return suggestion_time

def get_session_and_time_objects(current_hour):
    if time(20, 0) <= current_hour <= time(23, 59, 59) or time(0, 0) <= current_hour <= time(9, 59):
        session = "Breakfast"
        time_objects = table_time.objects.filter(time__in=[time(7, 0, 0), time(8, 0, 0), time(9, 0, 0)])
    if time(10, 0) <= current_hour <= time(13, 59):
        session = "Lunch"
        time_objects = table_time.objects.filter(time__in=[time(11, 0, 0), time(12, 0, 0), time(13, 0, 0)])
    if time(14, 0) <= current_hour <= time(19, 59):
        session = "Dinner"
        time_objects = table_time.objects.filter(time__in=[time(17, 0, 0), time(18, 0, 0), time(19, 0, 0)])
    return session, time_objects
