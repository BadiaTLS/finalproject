import pandas as pd
import random

# Check if data_dummy_session_menu.xlsx exists and retrieve session IDs
try:
    session_data = pd.read_excel("data_dummy_session_menu.xlsx")
    session_ids = session_data.index.tolist()
except FileNotFoundError:
    print("data_dummy_session_menu.xlsx not found.")
    session_ids = []

# Check if data_dummy_users.xlsx exists and retrieve user IDs and roles
try:
    user_data = pd.read_excel("data_dummy_users.xlsx")
    user_ids = user_data.index.tolist()
    user_roles = user_data["role"].tolist()
except FileNotFoundError:
    print("data_dummy_users.xlsx not found.")
    user_ids = []
    user_roles = []

# Exclude users with role dininghall
user_ids = [user_id for user_id, role in zip(user_ids, user_roles) if role != "dininghall"]

# Filter sessions with name breakfast, lunch, and dinner
breakfast_sessions = session_data[session_data["Name"] == "Breakfast"]
breakfast_session_ids = breakfast_sessions.index.tolist()
lunch_sessions = session_data[session_data["Name"] == "Lunch"]
lunch_session_ids = lunch_sessions.index.tolist()
dinner_sessions = session_data[session_data["Name"] == "Dinner"]
dinner_session_ids = dinner_sessions.index.tolist()

# Create list of times for breakfast, lunch, and dinner
breakfast_times = ["07:00:00", "07:30:00", "08:00:00", "08:30:00"]
lunch_times_1 = ["11:00:00", "11:30:00"]
lunch_times_2 = ["12:00:00", "12:30:00", "13:00:00"]
lunch_times_3 = ["13:30:00"]
dinner_times = ["17:00:00", "17:30:00", "18:00:00", "18:30:00", "19:00:00", "19:30:00"]

# Generate data for breakfast
data = []
id_counter = 0
for session_id in breakfast_session_ids:
    for time in breakfast_times:
        num_bookings = random.randint(2, 5) # How many time value in breakfast_times generated
        for i in range(num_bookings):
            user_id = random.choice(user_ids)
            data.append({
                "Recommended Time": time,
                "User ID": user_id+1,
                "Session ID": session_id+1
            })
            id_counter += 1

# Initialize an empty set to track user_ids for each session_id
session_bookings = {}

# Generate data for lunch
for session_id in lunch_session_ids:
    # Generate data for 11:00 and 11:30
    for time in lunch_times_1:
        num_bookings = random.randint(2, 4)
        num_bookings = random.randint(2, 4) # How many time value in lunch_times_1 generated      
        for i in range(num_bookings):
            user_id = random.choice(user_ids)

            # Check if user_id has booked for this session_id
            if session_id in session_bookings and user_id in session_bookings[session_id]:        
                continue  # Skip this booking, as the user has already booked for this session_id 
            else:
                # Add user_id to the set for this session_id
                if session_id not in session_bookings:
                    session_bookings[session_id] = set()
                session_bookings[session_id].add(user_id)
                data.append({
                    "Recommended Time": time,
                    "User ID": user_id + 1,
                    "Session ID": session_id + 1
                })
                id_counter += 1
            data.append({
                "Recommended Time": time,
                "User ID": user_id+1,
                "Session ID": session_id+1
            })
            id_counter += 1
    # Generate data for 12:00, 12:30, and 13:00
    for time in lunch_times_2:
        num_bookings = random.randint(4, 5)
        num_bookings = random.randint(4, 5) # How many time value in lunch_times_2 generated      
        for i in range(num_bookings):
            user_id = random.choice(user_ids)

            if session_id in session_bookings and user_id in session_bookings[session_id]:        
                continue
            else:
                if session_id not in session_bookings:
                    session_bookings[session_id] = set()
                session_bookings[session_id].add(user_id)

                data.append({
                    "Recommended Time": time,
                    "User ID": user_id + 1,
                    "Session ID": session_id + 1
                })
                id_counter += 1
            data.append({
                "Recommended Time": time,
                "User ID": user_id+1,
                "Session ID": session_id+1
            })
            id_counter += 1

    # Generate data for 13:30
    for time in lunch_times_3:
        num_bookings = random.randint(2, 4)
        num_bookings = random.randint(2, 4) # How many time value in lunch_times_3 generated      
        for i in range(num_bookings):
            user_id = random.choice(user_ids)

            if session_id in session_bookings and user_id in session_bookings[session_id]:        
                continue
            else:
                if session_id not in session_bookings:
                    session_bookings[session_id] = set()
                session_bookings[session_id].add(user_id)

                data.append({
                    "Recommended Time": time,
                    "User ID": user_id + 1,
                    "Session ID": session_id + 1
                })
                id_counter += 1
            data.append({
                "Recommended Time": time,
                "User ID": user_id+1,
                "Session ID": session_id+1
            })
            id_counter += 1

# Generate data for dinner
for session_id in dinner_session_ids:
    for time in dinner_times:
        num_bookings = random.randint(2, 5) # How many time value in dinner_times generated
        for i in range(num_bookings):
            user_id = random.choice(user_ids)
            data.append({
                "Recommended Time": time,
                "User ID": user_id+1,
                "Session ID": session_id+1
            })
            id_counter += 1

# Create DataFrame and export to excel
bookings_data = pd.DataFrame(data)
bookings_data.to_excel("data_dummy_bookings.xlsx", index=False)

print("Bookings Generated Successfully")
