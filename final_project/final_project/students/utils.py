from datetime import datetime, time, timedelta
from final_project.accounts.models import CustomUser
from final_project.dininghall.models import table_time, table_menu, table_booking_dininghall

def get_current_hour_and_current_date():
    current_hour = time(11,0,0) #datetime.now().time()
    current_date = datetime(2023, 6, 6)#datetime.now().date()
    if time(20, 0) <= current_hour <= time(23, 59, 59):
        current_date += timedelta(days=1)
    return current_hour, current_date

def get_suggestion_time():
    suggestion_time = time(12,45,0)
    return suggestion_time

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

def get_menu_based_date_and_session(date, session):
    menu = table_menu.objects.filter(date=date, session=session).first()
    return menu

def get_menu_based_menu(menu):
    booking = table_booking_dininghall.objects.filter(menu=menu)
    return booking

def get_menu_based_date(date):
    menus = table_menu.objects.filter(date=date)
    return menus

def get_student_based_username(username):
    student = CustomUser.objects.get(username=username)
    return student

def return_menus_for_each_session_in_one_date(menus):
    breakfast = None
    lunch = None
    dinner = None

    if not menus.filter(session="Breakfast"):
        breakfast = "Tidak ada breakfast"
    else:
        breakfast = list(menus.filter(session="Breakfast").values_list('menu', flat=True))[0]
    
    if not menus.filter(session="Lunch"):
        lunch = "Tidak ada lunch"
    else:
        lunch = list(menus.filter(session="Lunch").values_list('menu', flat=True))[0]

    if not menus.filter(session="Dinner"):
        dinner = "Tidak ada dinner"
    else:
        dinner = list(menus.filter(session="Dinner").values_list('menu', flat=True))[0]
    
    return breakfast, lunch, dinner

def is_within_restricted_range(booked_suggestion_time, current_hour):
    return (
        (time(7, 0, 0) <= booked_suggestion_time <= time(8, 59, 59) and current_hour < time(9, 0, 0) or current_hour > time(19, 0, 0))
        or (time(11, 0, 0) <= booked_suggestion_time <= time(13, 59, 59) and current_hour < time(14, 0, 0))
        or (time(17, 0, 0) <= booked_suggestion_time <= time(18, 59, 59) and current_hour < time(19, 0, 0))
    )

def get_session_and_time_objects(current_hour):
    if time(20, 0) <= current_hour <= time(23, 59, 59) or time(0, 0) <= current_hour <= time(9, 59):
        session = "Breakfast"
        time_objects = table_time.objects.filter(time__gte=time(7, 0, 0), time__lte=time(9, 30, 0))
    if time(10, 0) <= current_hour <= time(13, 59):
        session = "Lunch"
        time_objects = table_time.objects.filter(time__gte=time(11, 0, 0), time__lte=time(13, 30, 0))
    if time(14, 0) <= current_hour <= time(19, 59):
        session = "Dinner"
        time_objects = table_time.objects.filter(time__gte=time(17, 0, 0), time__lte=time(18, 30, 0))
    return session, time_objects

def get_student_dininghall_context(request):
    session = None
    current_hour, current_date = get_current_hour_and_current_date()
    session, time_objects = get_session_and_time_objects(current_hour)
    menu_object = get_menu_based_date_and_session(current_date, session)
    suggestion_time = get_suggestion_time().strftime('%H:%M:%S')
    has_booked = table_booking_dininghall.objects.filter(students_nim=request.user).exists()
    menus = get_menu_based_date(current_date)
    breakfast, lunch, dinner = return_menus_for_each_session_in_one_date(menus)
    can_book = True

    if has_booked:
        latest_booking = get_latest_booking(request.user)
        booked_suggestion_time = latest_booking.time_booked
        menu = latest_booking.menu
        booked_menu = menu.menu
        booked_session = menu.session

        if is_within_restricted_range(booked_suggestion_time, current_hour):
            can_book = False
            context = {
                'session': booked_session,
                'menu_object': booked_menu,
                'time_suggested': booked_suggestion_time.strftime('%H:%M:%S'),
                'day': current_date.strftime('%A'),
                'can_booking': can_book
            }
            return context
    
    context = {
        'time_objects': time_objects,
        'menu_object': menu_object,
        'time_suggested': suggestion_time,
        'session': session,
        'date': current_date,
        'day': current_date.strftime('%A'),
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'can_booking': can_book
    }
    return context
