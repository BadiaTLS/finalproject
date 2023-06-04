from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.db import transaction
from django.contrib import messages
from .utils import *

def check_student_role(user):
    return user.role == 'student'

@login_required(login_url='login')
@user_passes_test(check_student_role, login_url='not_student')
def students_index(request):
    return render(request, "students/student_index.html")

@login_required(login_url='login')
@user_passes_test(check_student_role, login_url='not_student')
def students_home_view_dininghall(request):
    context = get_student_dininghall_context(request)
    return render(request, 'students/student_dininghall_view.html', context)

@login_required(login_url='login')
@user_passes_test(check_student_role, login_url='not_student')
def students_home_view_library(request):
    return render(request, 'students/student_library_view.html')

@login_required(login_url='login')
@user_passes_test(check_student_role, login_url='not_student')
def students_home_view_laboratorium(request):
    return render(request, 'students/student_laboratorium_view.html')

@login_required(login_url='login')
@user_passes_test(check_student_role, login_url='not_student')
@transaction.atomic
def confirm_take_choice(request, current_hour, current_date, session, time_objects, menu_object):
    time_suggested = request.POST.get('time_suggested')
    student = get_student_based_username(username=request.user.username)
    menu = get_menu_based_date_and_session(current_date, session)

    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice == 'take':
            booking = get_menu_based_menu(menu)
            if booking.exists():
                latest_booking = get_latest_booking_for_menu(menu)
                vacancy = latest_booking.available - 1
                if latest_booking.available == 0:
                    messages.warning(request, 'The vacancy is already full.')
                    return redirect('dining_hall')
            else:
                vacancy = menu.limit - 1

            booking = create_booking(student, menu, vacancy, time_suggested)
            return redirect('dining_hall')
    
    context = {
        'time_objects': time_objects,
        'menu_object': menu_object,
        'time_suggested': time_suggested,
        'session': session,
        'date': current_date,
        'current_hour': current_hour,
        'can_booking': True
    }
    return render(request, 'students/student_preferences.html', context)

@login_required(login_url='login')
@user_passes_test(check_student_role, login_url='not_student')
@transaction.atomic
def student_preferences(request):
    if request.method == 'POST':
        take_value = request.POST.get('take')
        start_range_value = request.POST.get('start_range')
        end_range_value = request.POST.get('end_range')
        if take_value != 'take':
            return redirect('dining_hall')
        else:
            current_hour, current_date = get_current_hour_and_current_date()
            session, time_objects = get_session_and_time_objects(current_hour)
            menu_object = get_menu_based_date_and_session(current_date, session)
            time_suggested = time(12, 30, 0).strftime('%H:%M:%S')
            menus = get_menu_based_date(current_date)
            breakfast, lunch, dinner = return_menus_for_each_session_in_one_date(menus)
            context = {
                'time_objects': time_objects,
                'menu_object': menu_object,
                'time_suggested': time_suggested,
                'session': session,
                'date': current_date,
                'day': current_date.strftime('%A'),
                'breakfast': breakfast,
                'lunch': lunch,
                'dinner': dinner,
                'can_booking': True
            }
            return render(request, 'students/student_dininghall_view.html', context)

@login_required(login_url='login')
@user_passes_test(check_student_role, login_url='not_student')
def confirm(request):
    current_hour, current_date = get_current_hour_and_current_date()
    session, time_objects = get_session_and_time_objects(current_hour)
    menu_object = get_menu_based_date_and_session(current_date, session)
    return confirm_take_choice(request, current_hour, current_date, session, time_objects, menu_object)

def not_student(request):
    messages.error(request, 'You are not authorized to access student resources. You need the Student role.')
    return redirect('dininghall_index')
