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
    context['fullname'] =  request.user.name
    context['time_suggested'] : time_ordered
    context['session'] : session
    context['email'] = request.user.email
    return render(request, "students/student_index.html", context )

@student_required
def student_menu_view(request):
    if request.method == 'GET':
        context = get_student_dininghall_context(request)
        menu_this_week = get_menu_this_week(date=context['date'])
        context['menu_this_week'] = menu_this_week
        context['email'] = request.user.email
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
    if is_seat_full(session_id=session_object, date=current_date, time=time_suggested):
        messages.success(request, f"Apologies, but {session_object.name} on {session_object.date} at {time_suggested} is already full.", extra_tags="warning")
        context = get_student_dininghall_context(request)
        context['email'] = request.user.email
        return redirect('student_index')

    time_object = get_time_by_session_id_and_suggested_time(time_suggested, session_object)
    if time_object is not None: 
        update_available_seats(time_object)
        user_object = get_userobject_by_id(request.user.id)
        create_booking(user_object, session_object, time_suggested)
        print('CONFIRM: Booking Success')
        messages.success(request, 
                        f"Booking Success for {session_object.name}, {session_object.date} at {time_suggested}", 
                        extra_tags="success")
        context = get_student_dininghall_context(request=request)
        context['can_booking'] = False
        return render(request=request, template_name= "students/student_dininghall_view.html", context=context)
        return redirect('student_index' ) 
        
    messages.success(request, f"Booking Failed for {session_object.name}, {session_object.date} at {time_suggested}", extra_tags="warning")

    return redirect('student_index') 

@student_required
@transaction.atomic
def cancel_order(request):
    if request.method == 'POST':
        user_object = request.user
        session_id = request.POST.get('o')
        print(session_id)
        session_object = table_session.objects.get(pk=session_id)
        message , extra_tags = delete_booking_and_update_available_seat_by_user_id(user_object, session_object)
        
        messages.success(request, message=message, extra_tags=extra_tags)
        return redirect("dining_hall")
    messages.success(request, message="The Method is GET", extra_tags="danger")
    return redirect("dining_hall")


@student_required
@transaction.atomic
def student_preferences(request):
    if request.method == 'POST':
        is_searching = request.POST.get('search_button_pressed')
        if is_searching:
            start_time = request.POST.get('start_range')
            end_time = request.POST.get('end_range')

            session = request.POST.get('session_pref')
            date_pref = request.POST.get('date_pref')
            date_pref = datetime.strptime(date_pref, "%Y-%m-%d").date()

            print(request.user.id, date_pref, session)
            if is_booked_by_user_date_session(request.user.id, date_pref, session):
                messages.success(request, f"You already booked {session} for {date_pref}.", extra_tags="danger")
                return redirect('student_preferences')

            current_hour, _ = get_current_hour_and_current_date()
            _s, time_objects = get_session_and_time_objects(current_hour)

            session_id = get_session_id_based_date_and_session_name(date_pref, session)
            session_info = get_session_time_and_seat(get_session_id(date_pref, session))

            if date_pref < _:
                messages.success(request, f"Apologies, but the {session} on {date_pref} is no longer available for booking, as the allotted time has elapsed.", extra_tags="danger")
                return redirect('student_preferences')
            
            try: 
                session_start_time = get_session_start_time(session_id=session_id.id)
            except:
                messages.success(request, f"Apologies, Options not available for {session} on {date_pref}", extra_tags="danger")
                return redirect('student_preferences')

            if date_pref == _ and current_hour > session_start_time:
                messages.success(request, f"Apologies, but the {session} on {date_pref} at {current_hour} is no longer available for booking, as the allotted time has elapsed.", extra_tags="danger")
                return redirect('student_preferences')
            
            start_time = datetime.strptime(start_time, "%H:%M").time()
            end_time = datetime.strptime(end_time, "%H:%M").time()

            suggested_time = get_recommended_time(session_info, start_time, end_time)

            context = {
                'time_objects': time_objects,
                'session_id': session_id,
                'time_suggested': suggested_time,
                'session': session,
                'date': date_pref,
                'day': date_pref.strftime('%A'),
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
            return confirm_action(request, current_hour, current_date, session, time_object, session_object)
        else:
            print("Confirm Data Not Valid")
            messages.success(request, "Oops! Invalid input. Please retry.", extra_tags="danger")
            return render(request, "students/student_preferences.html")
    else:
        messages.success(request, "Send Some POST data", extra_tags="danger")    
        return redirect("student_index")


# Start Bookings Table
@student_required
def show_bookings(request):
    context = get_bookings(request=request)
    return render(request, 'students/bookings_page.html', context)

@student_required
def delete_booking(request, booking_id):
    from django.shortcuts import get_object_or_404
    booking = get_object_or_404(table_booking_dininghall, pk=booking_id)
    session_id = booking.session_id
    recommended_time = booking.recommended_time

    booked_time = table_time.objects.get(session_id=session_id, time=recommended_time)
    booked_time.available_seat += 1
    booked_time.save()
    booking.delete()
    return redirect('show_bookings')

def not_student(request):
    messages.error(request, 'You are not authorized to access student resources. You need the Student role.')
    return redirect('login')
