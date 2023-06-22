from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.db import transaction
from django.contrib import messages
from .utils import *
from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test

def check_student_role(user):
    return user.role == 'student' or user.role == 'dosen'

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
    time_ordered, session = get_order_time(request.user.id)
    context = get_student_dininghall_context(request)
    context['email'] = request.user.email
    context['fullname'] =  request.user.name
    context['time_suggested'] : time_ordered
    context['session'] : session
    
    return render(request, "students/student_index.html", context )

@student_required
def menu(request):
    context = get_student_dininghall_context(request)
    return render(request, 'students/menu.html', context)

@student_required
def students_home_view_dininghall(request):
    context = get_student_dininghall_context(request)
    context['email'] = request.user.email
    return render(request, 'students/student_dininghall_view.html', context)

@student_required
def students_home_view_library(request):
    context = {'email': request.user.email}
    return render(request, 'students/student_library_view.html', context)

@student_required
def students_home_view_laboratorium(request):
    context = {'email': request.user.email}
    return render(request, 'students/student_laboratorium_view.html', context)

@student_required
@transaction.atomic
def confirm_action(request, current_hour, current_date, session_name, time_objects, session_object):
    print("Confirm Action Called")
    print(type(current_hour), type(current_date), type(session_name), type(time_objects), type(session_object))
    session_object = get_session_id_based_date_and_session_name(current_date, session_name)
    time_suggested = request.POST.get('time_suggested')
    choice = request.POST.get('choice')
    if choice == 'no':
        context = {
            'time_objects': time_objects,
            'session_object': session_object,
            'time_suggested': time_suggested,
            'session': session_name,
            'date': current_date,
            'current_hour': current_hour,
            'can_booking': True
        }
        return render(request, 'students/student_preferences.html', context)

    time_object = get_time_by_session_id_and_suggested_time(time_suggested, session_object)
    print("CONFIRM ACTION ", time_object, time_suggested, session_object, type(session_object))
    if time_object is not None: 
        update_available_seats(time_object)
        user_object = get_userobject_by_id(request.user.id)
        create_booking(user_object, session_object, time_suggested)
        print('booking success')
        # update_seat_availability(time_suggested, new_availability_seat)
        messages.success(request, 
                        f"Booking Success for {session_object.name}, {session_object.date} at {time_suggested}", 
                        extra_tags="success")
        return redirect('student_index') 
        
    messages.success(request, f"Booking Failed for {session_object.name}, {session_object.date} at {time_suggested}", extra_tags="warning")

    return redirect('student_index') 


@student_required
@transaction.atomic
def cancel_order(request):
    user_id = request.user.id
    # DELETE and UPDATE Database
    message = delete_booking_and_update_available_seat_by_user_id(user_id)
    messages.success(request, message, extra_tags="success")
    
    return redirect("student_index")

@student_required
@transaction.atomic
def student_preferences(request):
    if request.method == 'POST':
        is_take = request.POST.get('take')
        if is_take:

            start_time = request.POST.get('start_range')
            end_time = request.POST.get('end_range')

            session = request.POST.get('session_pref')
            date_pref = request.POST.get('date_pref')
            current_date = datetime.strptime(date_pref, "%Y-%m-%d").date()

            current_hour, _ = get_current_hour_and_current_date()
            _, time_objects = get_session_and_time_objects(current_hour)

            session_id = get_session_id_based_date_and_session_name(current_date, session)
            session_info = get_session_time_and_seat(get_session_id(current_date, session))

            suggested_time = get_recommended_time(session_info, start_time, end_time)
            menus = get_menu_based_date(current_date)
            breakfast, lunch, dinner = get_menu_b_l_d(menus)
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
                'current_session' : session.upper(),
                'email' : request.user.email,
            }
            return render(request, 'students/student_preferences.html', context)
    
    if request.method == 'GET':
        
        start_time = request.POST.get('start_range')
        end_time = request.POST.get('end_range')

        current_hour, current_date = get_current_hour_and_current_date()
        session, time_objects = get_session_and_time_objects(current_hour)

        session_id = get_session_id_based_date_and_session_name(current_date, session)
        session_info = get_session_time_and_seat(get_session_id(current_date, session))

        request.POST.get('time_suggested')
        context = {
                'time_objects': time_objects,
                'session_id': session_id,
                'time_suggested': "NotSearched",
                'session': session,
                'date': current_date,
                'day': current_date.strftime('%A'),
                'can_booking': True,
                'current_session' : session.upper(),
                'email' : request.user.email,
            }
        return render(request, 'students/student_preferences.html', context)
    


@student_required
def confirm(request):
    from .forms import ConfirmForm
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = ConfirmForm(request.POST)

        time_object = request.POST.get('time_object')
        session_object = request.POST.get('session_object')
        current_date = request.POST.get('current_date')
        current_hour = request.POST.get('current_hour')
        current_hour, _ = get_current_hour_and_current_date()
        session = request.POST.get('session')
        print(time_object, session_object, current_date, session)

        # Check if the form is valid
        if form.is_valid():
            # Get the values of the form fields
            time_object = form.cleaned_data['time_object']
            session_object = form.cleaned_data['session_object']
            current_date = form.cleaned_data['current_date']
            session = request.POST.get('session')

            session_object = get_session_id_based_date_and_session_name(current_date, session)
            time_object = get_time_by_session_id_and_suggested_time(time_object, session_object)

            # Do something with the values
            print(time_object, current_date, current_hour, session, session_object)
            return confirm_action(request, current_hour, current_date, session, time_object, session_object)
        else:
            print("Confirm Data Not Valid")
            messages.success(request, "Oops! Invalid input. Please retry.", extra_tags="danger")
            return render(request, "students/student_preferences.html")
            current_hour, current_date = get_current_hour_and_current_date()
            session, time_objects = get_session_and_time_objects(current_hour)
            session_id = get_session_id_based_date_and_session_name(current_date, session)
            # messages.success(request, "Input not valid, retry again", extra_tags="warning")
            return confirm_action(request, current_hour, current_date, session, time_objects, session_id)
    else:
        print("Send POST")
        messages.success(request, "Send Some POST data", extra_tags="danger")    
        return redirect("student_index")


# @student_required
# def confirm(request):
#     if request.method == 'POST':
#         current_hour = request.POST.get('current_hour')
#         current_date = request.POST.get('current_date')
#         time_objects = request.POST.get('time_object')
#         session_object = request.POST.get('session_id')
#         session_name = request.POST.get('session')
#         print(type(current_hour), type(current_date), type(session_name), type(time_objects), type(session_object))

#         # try: 
#         #     print("CONFRIM: ")
#         #     return confirm_action(request, current_hour, current_date, session_name, time_objects, session_object)
#         # except:
#         #     current_hour, current_date = get_current_hour_and_current_date()
#         #     session, time_objects = get_session_and_time_objects(current_hour)
#         #     session_id = get_session_id_based_date_and_session_name(current_date, session)
#         return confirm_action(request, current_hour, current_date, session_name, time_objects, session_object)

def not_student(request):
    messages.error(request, 'You are not authorized to access student resources. You need the Student role.')
    return redirect('dininghall_index')
