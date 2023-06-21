from datetime import datetime, time, timedelta
from final_project.accounts.models import CustomUser
from final_project.dininghall.models import table_time, table_session, table_booking_dininghall
from final_project.sas.models import table_classes
from final_project.algorithm.dijkstra import get_recommended_time
import json

# CHECK
def is_time_booked(request):
    result = table_booking_dininghall.objects.filter(user_id=request.user.id).exists()
    if result: 
        return False
    return True

def is_session_id_in_booking_table(session_id):
    booking = table_booking_dininghall.objects.filter(session_id=session_id)
    if not booking.exists():
        return False
    return True

def is_within_restricted_range(booked_suggestion_time, current_hour):
    return (
        (time(7, 0, 0) <= booked_suggestion_time <= time(8, 59, 59) and current_hour < time(9, 0, 0) or current_hour > time(19, 0, 0))
        or (time(11, 0, 0) <= booked_suggestion_time <= time(13, 59, 59) and current_hour < time(14, 0, 0))
        or (time(17, 0, 0) <= booked_suggestion_time <= time(18, 59, 59) and current_hour < time(19, 0, 0))
    )

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time < time_range[1]
    return time_range[0] <= time < time_range[1]

# GET
def get_userobject_by_id(id):
    user_object = CustomUser.objects.get(id=id)
    return user_object

def get_order_time(user_id):
    booking = table_booking_dininghall.objects.filter(user_id=user_id).first()
    if booking:
        recommended_time = booking.recommended_time
        session_name = booking.session_id.name
        return recommended_time, session_name
    else:
        return None, 0

def get_current_hour_and_current_date():
    # Setup Manual
    # current_hour = time(11,0,0) #datetime.now().time()
    # current_date = datetime(2023,6,6) #datetime.now().date()

    # Automatic
    
    current_hour = datetime.now().time()
    current_date = datetime.now().date()

    if time(20, 0) <= current_hour <= time(23, 59, 59):
        current_date += timedelta(days=1)
    return current_hour, current_date

def get_latest_booking_for_menu(menu):
    latest_booking_for_menu = table_booking_dininghall.objects.filter(session_id=menu).latest('id')
    return latest_booking_for_menu

def get_latest_booking(user_id):
    # This will return the object
    try: 
        latest_booking = table_booking_dininghall.objects.filter(user_id=user_id).latest('created_at')
        return latest_booking
    except:
        return False

def get_session_id_based_date_and_session_name(date, session_name):
    session_id = table_session.objects.filter(date=date, name=session_name).first()
    return session_id

def get_time_by_session_id_and_suggested_time(time, session_id):
    time_object = table_time.objects.filter(time = time, session_id=session_id).first()
    return time_object 

def get_menu_based_date(date):
    menus = table_session.objects.filter(date=date)
    return menus

def get_week_dates(date_str):
    # parse the input date string
    if type(date_str) == str:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    else:
        date = date_str

    # calculate the start of the week (Monday)
    start_of_week = date - timedelta(days=date.weekday())

    # generate a list of dates for the entire week
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

    # format the dates as strings
    # week_dates_str = [date.strftime('%Y-%m-%d') for date in week_dates]

    return week_dates

def generate_menu_data(meal_name, date, menu):
    day_name = date.strftime('%A')
    return {
        'day': day_name,
        'date': f'{menu}'  ,
        'imgSrc': f'img/{meal_name.lower()}-{day_name.lower()}.jpg',
        'altText': '',
        'name': f'{day_name} {meal_name.capitalize()}',
        'price': '$115',
        'description': f'{date}'
    }

def get_menu_this_week(date):

    # example usage
    week_dates = get_week_dates(date)
    # print(week_dates)

    breakfast = []
    lunch = []
    dinner = []

    for date in week_dates:
        menus = get_menu_based_date(date)
        b, l, d = return_menus_for_each_session_in_one_date(menus)
        breakfast.append(b)
        lunch.append(l)
        dinner.append(d)
    # print(breakfast, lunch, dinner)
    
    tabs_data = {
        'tab-1': [],
        'tab-2': [],
        'tab-3': []
    }
    for i, date in enumerate(week_dates):
        tabs_data['tab-1'].append(generate_menu_data('breakfast', date, breakfast[i]))
        tabs_data['tab-2'].append(generate_menu_data('lunch', date, lunch[i]))
        tabs_data['tab-3'].append(generate_menu_data('dinner', date, dinner[i]))

    # print(tabs_data)
    # convert the tabs_data dictionary to a JSON string
    menu_data_json = json.dumps(tabs_data)

    return menu_data_json

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
    session = table_session.objects.filter(date=date, name=name).first()
    if session:
        return session.id
    else:
        return None

def get_classes_by_day(day):
    list_class = table_classes.objects.filter(class_day = day)
    return list_class

def get_classes_by_email(email, class_list):
    classes_that_email_is_in = []

    for class_object in class_list:
        if class_object.attendees.filter(email=email).exists():
            classes_that_email_is_in.append(class_object)

    return classes_that_email_is_in

def get_start_end_for_algorithm(email, day, session_times):
    try: 
        day = translate_day_to_en(day).lower()
    except:
        day = day.lower()

    class_list = get_classes_by_day(day)
    class_list_by_email = get_classes_by_email(email, class_list)

    # print(f"Kelas Hari ini {day}: {class_list}\n Kelas yang dihadiri {email}: {class_list_by_email}")


    # Get The classes for the day
    for i in class_list_by_email:
        for session_time in session_times:
            if is_between(session_time, (i.class_start_time, i.class_end_time)):
                session_times[session_time] = 0
                # print(session_times[session_time])
                # print(f"{session_time} is between {i.class_start_time} and {i.class_end_time}")
            else:
                pass
                # print(f"{session_time} is not between {i.class_start_time} and {i.class_end_time}")    

    # start = class_list_by_email[0].class_start_time
    # end = class_list_by_email[0].class_end_time
    start, end = list(session_times.keys())[0], list(session_times.keys())[-1]

    # print(start, end, email, day, session_times)
    return start, end, session_times

def get_student_dininghall_context(request):
    current_hour, current_date = get_current_hour_and_current_date()
    session, time_objects = get_session_and_time_objects(current_hour)
    
    session_id = get_session_id(current_date, session)
    if session_id:
        suggestion_time = get_suggestion_time(session_id, request.user.email, current_date)
    else:
        suggestion_time = None

    latest_booking = get_latest_booking(request.user)
    if latest_booking:
        context = get_context_from_latest_booking(latest_booking, current_hour, current_date)
        if context:
            return context
    
    menus = get_menu_based_date(current_date)
    breakfast, lunch, dinner = return_menus_for_each_session_in_one_date(menus)
    menu_this_week = get_menu_this_week(current_date)

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
        'can_booking': True,
        'current_session' : session.upper(),
        # Here we can add more... Like Menus
        'menu_this_week' : menu_this_week
    }
    return context

def get_suggestion_time(session_object, email, current_date):
    session_info = get_session_time_and_seat(session_object)

    day = current_date.strftime('%A')
    day = translate_day(day)

    start, end, session_info = get_start_end_for_algorithm(email, day, session_info)
    suggestion_time = get_recommended_time(session_info, start, end)
    
    return suggestion_time

def get_context_from_latest_booking(latest_booking, current_hour, current_date):
    print(latest_booking, current_hour, current_date)

    booked_suggestion_time = latest_booking.recommended_time
    menu = latest_booking.session_id
    booked_menu = menu.menu
    booked_session = menu.name


    if is_within_restricted_range(booked_suggestion_time, current_hour):
        context = {
            'session': booked_session,
            'session_id': booked_menu,
            'date' : menu.date,
            'time_suggested': booked_suggestion_time.strftime('%H:%M'),
            'day': current_date.strftime('%A'),
            'can_booking': False,
            'menu_this_week': get_menu_this_week(current_date)
        }
        return context

# NON GET and CHECK
def create_booking(user_id, session_id, time_suggested):
    booking = table_booking_dininghall.objects.create(
        user_id=user_id,
        session_id=session_id,
        recommended_time=time_suggested,
    )
    booking.save()
    return booking

def translate_day(day):
    days = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }
    return days.get(day)

def translate_day_to_en(day):
    days = {
        "Senin": "Monday",
        "Selasa": "Tuesday",
        "Rabu": "Wednesday",
        "Kamis": "Thursday",
        "Jumat": "Friday",
        "Sabtu": "Saturday",
        "Minggu": "Sunday"
    }
    return days.get(day)

def update_available_seats(time):
    if time.available_seat == 0:
        raise ValueError("Not enough available seats")
    time.available_seat = (time.available_seat or time.seat_limit) - 1
    time.save()
    return time 

def return_menus_for_each_session_in_one_date(menus):
    meals = {}
    for meal_name in ["Breakfast", "Lunch", "Dinner"]:
        if not menus.filter(name=meal_name):
            meals[meal_name] = f"Tidak ada {meal_name.lower()}"
        else:
            meals[meal_name] = menus.filter(name=meal_name).first().menu
    return meals["Breakfast"], meals["Lunch"], meals["Dinner"]

def delete_booking_and_update_available_seat_by_user_id(user_id):
    try: 
        booking_object = table_booking_dininghall.objects.filter(user_id=user_id).latest('created_at')
        
        session_id = booking_object.session_id
        recommended_time = booking_object.recommended_time

        booked_time_object = table_time.objects.get(session_id=session_id, time = recommended_time)
        booked_time_object.available_seat += 1
        booked_time_object.save()
        booking_object.delete()
        return "Success: Booking Deleted and Available Seat Updated" 
    except: 
        return "Failed: Booking Deleted and Available Seat Updated "
