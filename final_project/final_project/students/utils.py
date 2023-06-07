from datetime import datetime, time, timedelta
from final_project.accounts.models import CustomUser
from final_project.dininghall.models import table_time, table_session, table_booking_dininghall
from final_project.algorithm.dijkstra import get_recommended_time

def get_current_hour_and_current_date():
    # Setup Manual
    current_hour = time(11,0,0) #datetime.now().time()
    current_date = datetime(2023,6,6) #datetime.now().date()

    # Automatic
    # current_hour = datetime.now().time()
    # current_date = datetime.now().date()

    if time(20, 0) <= current_hour <= time(23, 59, 59):
        current_date += timedelta(days=1)
    return current_hour, current_date

def create_booking(student, session_id, time_suggested):
    booking = table_booking_dininghall.objects.create(
        user_id=student,
        session_id=session_id,
        recommended_time=time_suggested,
    )
    session_id.save()
    return booking

def get_latest_booking_for_menu(menu):
    latest_booking_for_menu = table_booking_dininghall.objects.filter(session_id=menu).latest('id')
    return latest_booking_for_menu

def get_latest_booking(user):
    latest_booking = table_booking_dininghall.objects.filter(user_id=user).latest('created_at')
    return latest_booking

def get_session_id_based_date_and_session_name(date, session_name):
    session_id = table_session.objects.filter(date=date, name=session_name).first()
    return session_id

def get_time_by_session_id_and_suggested_time(time, session_id):
    time_object = table_time.objects.filter(time = time, session_id=session_id).first()
    return time_object 

def is_session_id_in_booking_table(session_id):
    booking = table_booking_dininghall.objects.filter(session_id=session_id)
    if not booking.exists():
        return False
    return True

def update_available_seats(time):
    if time.available_seat == 0:
        raise ValueError("Not enough available seats")
    if time.available_seat == None: 
        time.available_seat = time.seat_limit -1
        time.save()
    else: 
        time.available_seat -= 1 
        time.save()
    return time 


# def get_menu_based_menu(session_id):
#     booking = table_booking_dininghall.objects.filter(session_id=session_id)
#     return booking

def get_menu_based_date(date):
    menus = table_session.objects.filter(date=date)
    return menus

def return_menus_for_each_session_in_one_date(menus):
    breakfast = None
    lunch = None
    dinner = None

    if not menus.filter(name="Breakfast"):
        breakfast = "Tidak ada breakfast"
    else:
        breakfast = menus.filter(name="Breakfast").first().menu
    
    if not menus.filter(name="Lunch"):
        lunch = "Tidak ada lunch"
    else:
        lunch = menus.filter(name="Lunch").first().menu

    if not menus.filter(name="Dinner"):
        dinner = "Tidak ada dinner"
    else:
        dinner = menus.filter(name="Dinner").first().menu
    
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
    elif time(10, 0) <= current_hour <= time(13, 59):
        session = "Lunch"
        time_objects = table_time.objects.filter(time__gte=time(11, 0, 0), time__lte=time(13, 30, 0))
    elif time(14, 0) <= current_hour <= time(19, 59):
        session = "Dinner"
        time_objects = table_time.objects.filter(time__gte=time(17, 0, 0), time__lte=time(18, 30, 0))
    else:
        session = None
        time_objects = []
    return session, time_objects

def get_session_time_and_seat(session_id):
    session = table_session.objects.get(id=session_id)
    times = table_time.objects.filter(session_id=session)
    session_time_and_seat = {}
    for time_obj in times:
        if time_obj.available_seat:
            session_time_and_seat[time_obj.time] = time_obj.available_seat
        else:
            session_time_and_seat[time_obj.time] = time_obj.seat_limit
    return session_time_and_seat

def get_session_id(date, name):
    session = table_session.objects.get(date=date, name=name)
    return session.id

def get_student_dininghall_context(request):
    current_hour, current_date = get_current_hour_and_current_date()
    session, time_objects = get_session_and_time_objects(current_hour)
    # session_id = get_session_id_based_date_and_session_name(current_date, session)
    
    # ALGORITHM START HERE #
    try: 
        session_id = get_session_id(current_date, session)
        session_info = get_session_time_and_seat(session_id)
        start = '11:00'
        end = '13:30'
        suggestion_time = get_recommended_time(session_info, start, end)

    except: 
        session_id = False
        session_info = None
        suggestion_time = None

    # ALGORITHM END HERE #


    has_booked = table_booking_dininghall.objects.filter(user_id=request.user).exists()
    menus = get_menu_based_date(current_date)
    breakfast, lunch, dinner = return_menus_for_each_session_in_one_date(menus)
    can_book = True

    if has_booked:
        latest_booking = get_latest_booking(request.user)
        booked_suggestion_time = latest_booking.recommended_time
        menu = latest_booking.session_id
        booked_menu = menu.menu
        booked_session = menu.name

        if is_within_restricted_range(booked_suggestion_time, current_hour):
            can_book = False
            context = {
                'session': booked_session,
                'session_id': booked_menu,
                'time_suggested': booked_suggestion_time.strftime('%H:%M:%S'),
                'day': current_date.strftime('%A'),
                'can_booking': can_book
            }
        return context
    
    context = {
        'time_objects': time_objects,
        'session_id': session_id,
        'time_suggested': suggestion_time,
        'session': session,
        'date': current_date,
        'day': current_date.strftime('%A'),
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'can_booking': can_book,
        'current_session' : session.upper()
        
    }
    return context
