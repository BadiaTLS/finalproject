from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.db import transaction
from django.contrib import messages
from .utils import *
from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test

def check_student_role(user):
    return user.role == 'student'

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        return login_required(
            user_passes_test(
                check_student_role,
                login_url='login'
            )(view_func)
        )(request, *args, **kwargs)
    return wrapper

@student_required
def students_index(request):
    fullname = {'fullname': request.user.name}
    print(fullname)

    return render(request, "students/student_index.html", fullname )

@student_required
def students_home_view_dininghall(request):
    context = get_student_dininghall_context(request)
    return render(request, 'students/student_dininghall_view.html', context)

@student_required
def students_home_view_library(request):
    return render(request, 'students/student_library_view.html')

@student_required
def students_home_view_laboratorium(request):
    return render(request, 'students/student_laboratorium_view.html')

@student_required
@transaction.atomic
def confirm_action(request, current_hour, current_date, session_name, time_objects, session_id):
    context = None
    time_suggested = request.POST.get('time_suggested')
    session_id = get_session_id_based_date_and_session_name(current_date, session_name)
    choice = request.POST.get('choice')

    if choice == 'no':
        context = {
            'time_objects': time_objects,
            'session_id': session_id,
            'time_suggested': time_suggested,
            'session': session_name,
            'date': current_date,
            'current_hour': current_hour,
            'can_booking': True
        }
        
        return render(request, 'students/student_preferences.html', context)
    
    if is_session_id_in_booking_table(session_id):
        context = None
        return render(request, 'students/student_preferences.html', context)
    
    time_object = get_time_by_session_id_and_suggested_time(time_suggested, session_id)
    print(time_object)
    if time_object is not None: 
        update_available_seats(time_object)
    # create_booking()
    # update_seat_availability(time_suggested, new_availability_seat)

    return redirect('dining_hall') 


@student_required
@transaction.atomic
def student_preferences(request):
    if request.method == 'POST':
        take_value = request.POST.get('take')
        start_time = request.POST.get('start_range')
        end_time = request.POST.get('end_range')
        if take_value != 'take':
            return redirect('dining_hall')
        else:
            current_hour, current_date = get_current_hour_and_current_date()
            session, time_objects = get_session_and_time_objects(current_hour)
            session_id = get_session_id_based_date_and_session_name(current_date, session)
            session_info = get_session_time_and_seat(get_session_id(current_date, session))
            suggested_time = get_recommended_time(session_info, start_time, end_time)
            menus = get_menu_based_date(current_date)
            breakfast, lunch, dinner = return_menus_for_each_session_in_one_date(menus)
            context = {
                'time_objects': time_objects,
                'session_id': session_id,
                'time_suggested': suggested_time,
                'session': session,
                'date': current_date,
                'day': current_date.strftime('%A'),
                'breakfast': breakfast,
                'lunch': lunch,
                'dinner': dinner,
                'can_booking': True,
                'current_session' : session.upper()

            }
            return render(request, 'students/student_dininghall_view.html', context)

@student_required
def confirm(request):
    current_hour, current_date = get_current_hour_and_current_date()
    session, time_objects = get_session_and_time_objects(current_hour)
    session_id = get_session_id_based_date_and_session_name(current_date, session)

    return confirm_action(request, current_hour, current_date, session, time_objects, session_id)

def not_student(request):
    messages.error(request, 'You are not authorized to access student resources. You need the Student role.')
    return redirect('dininghall_index')
