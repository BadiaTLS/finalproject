import pandas as pd
import random

def read_session_data():
    try:
        session_data = pd.read_excel("data_dummy_session.xlsx")
        session_ids = session_data.index.tolist()
        return session_data, session_ids
    except FileNotFoundError:
        print("data_dummy_session.xlsx not found.")
        return None, []

def read_user_data():
    try:
        user_data = pd.read_excel("data_dummy_users.xlsx")
        user_ids = user_data.index.tolist()
        user_roles = user_data["role"].tolist()
        return user_data, user_ids, user_roles
    except FileNotFoundError:
        print("data_dummy_users.xlsx not found.")
        return None, [], []

def filter_user_roles(user_ids, user_roles):
    return [user_id for user_id, role in zip(user_ids, user_roles) if role != "dininghall"]

def filter_session_data(session_data, session_name):
    return session_data[session_data["Name"] == session_name]

def generate_data(session_ids, times, num_bookings_range, user_ids):
    data = []
    id_counter = 0

    for session_id in session_ids:
        for time in times:
            num_bookings = random.randint(*num_bookings_range)
            for _ in range(num_bookings):
                user_id = random.choice(user_ids)
                data.append({
                    "Recommended Time": time,
                    "User ID": user_id + 1,
                    "Session ID": session_id + 1
                })
                id_counter += 1

    return data

def generate_bookings():
    session_data, session_ids = read_session_data()
    user_data, user_ids, user_roles = read_user_data()

    if session_data is None or user_data is None:
        return

    user_ids = filter_user_roles(user_ids, user_roles)

    breakfast_sessions = filter_session_data(session_data, "Breakfast")
    breakfast_session_ids = breakfast_sessions.index.tolist()
    lunch_sessions = filter_session_data(session_data, "Lunch")
    lunch_session_ids = lunch_sessions.index.tolist()
    dinner_sessions = filter_session_data(session_data, "Dinner")
    dinner_session_ids = dinner_sessions.index.tolist()

    breakfast_times = ["07:00:00", "07:30:00", "08:00:00", "08:30:00"]
    lunch_times_1 = ["11:00:00", "11:30:00"]
    lunch_times_2 = ["12:00:00", "12:30:00", "13:00:00"]
    lunch_times_3 = ["13:30:00"]
    dinner_times = ["17:00:00", "17:30:00", "18:00:00", "18:30:00", "19:00:00", "19:30:00"]

    data = []

    data.extend(generate_data(breakfast_session_ids, breakfast_times, (2, 5), user_ids))
    data.extend(generate_data(lunch_session_ids, lunch_times_1, (2, 4), user_ids))
    data.extend(generate_data(lunch_session_ids, lunch_times_2, (4, 5), user_ids))
    data.extend(generate_data(lunch_session_ids, lunch_times_3, (2, 4), user_ids))
    data.extend(generate_data(dinner_session_ids, dinner_times, (2, 5), user_ids))

    bookings_data = pd.DataFrame(data)
    bookings_data.to_excel("data_dummy_bookings.xlsx", index=False)

    print("Bookings Generated Successfully")

# Call the function to generate bookings
generate_bookings()
