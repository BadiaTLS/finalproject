from django.shortcuts import render, redirect
from datetime import datetime, time, timedelta
from final_project.dininghall.models import table_time, table_menu, table_booking_dininghall
from final_project.students.models import table_students_information
from django.db import transaction
from django.contrib import messages

# Create your views here.
def students_index(request):
    return render(request, "students/student_index.html")

def get_suggestion_time():
    suggestion_time = time(7,30,0)
    return suggestion_time

def students_home_view_dininghall(request):
    current_hour = datetime.now().time()
    current_date = datetime.now().date()
    session, time_objects, current_date = get_session_and_time_objects(current_hour, current_date)
    menu_object = table_menu.objects.filter(date=current_date, session=session).first()
    suggestion_time = get_suggestion_time().strftime('%H:%M:%S')
    context = {'time_objects': time_objects, 'menu_object': menu_object, 'time_suggested': suggestion_time, 'session':session, 'date':current_date}
    return render(request, 'students/student_dininghall_view.html', context)

def students_home_view_library(request):
    return render(request, 'students/student_library_view.html')

def students_home_view_laboratorium(request):
    return render(request, 'students/student_laboratorium_view.html')

@transaction.atomic
def confirm(request):
    current_hour = datetime.now().time()
    current_date = datetime.now().date()
    session, time_objects, current_date = get_session_and_time_objects(current_hour, current_date)
    if request.method == 'POST':
        time_suggested = request.POST.get('time_suggested')
        choice = request.POST.get('choice')
        student_nim = table_students_information.objects.get(nim=191900602)
        menu = table_menu.objects.get(date=current_date, session=session)
        if choice == 'take':
            booking = table_booking_dininghall.objects.filter(menu=menu)
            if booking.exists():
                latest_booking = booking.latest('id')
                vacancy = latest_booking.vacancy - 1
                if booking.latest('id').vacancy == 0:
                    messages.warning(request, 'The vacancy is already full.')
                    return redirect('dining_hall')
            else:
                vacancy = menu.vacancy - 1
            booking = table_booking_dininghall.objects.create(vacancy=vacancy, time_booked=time_suggested, menu=menu)
            booking.students_nim.add(student_nim)
            return redirect('dining_hall')
        else:
            return render(request, 'students/student_preferences.html', {'current_hour':current_hour})
        
    return render(request, 'students/student_dininghall_view.html')

@transaction.atomic
def student_preferences(request):
    if request.method == 'POST':
        take_value = request.POST.get('take')
        start_range_value = request.POST.get('start_range')
        end_range_value = request.POST.get('end_range')
        if take_value != 'take':
            return redirect('dining_hall')
        else:
            pass

def get_session_and_time_objects(current_hour, current_date):
    if time(20, 0) <= current_hour <= time(23, 59, 59) or time(0, 0) <= current_hour <= time(9, 59):
        session = "Breakfast"
        time_objects = table_time.objects.filter(time__in=[time(7, 0, 0), time(8, 0, 0), time(9, 0, 0)])
        if time(20, 0) <= current_hour <= time(23, 59, 59):
            current_date += timedelta(days=1)
        else:
            pass
    if time(10, 0) <= current_hour <= time(13, 59):
        session = "Lunch"
        time_objects = table_time.objects.filter(time__in=[time(11, 0, 0), time(12, 0, 0), time(13, 0, 0)])
    if time(14, 0) <= current_hour <= time(19, 59):
        session = "Dinner"
        time_objects = table_time.objects.filter(time__in=[time(17, 0, 0), time(18, 0, 0), time(19, 0, 0)])

    return session, time_objects, current_date