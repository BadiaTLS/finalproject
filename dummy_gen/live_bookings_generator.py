import pandas as pd
from datetime import timedelta, datetime
import random

# Check if data_dummy_bookings.xlsx exists and retrieve booking IDs
try:
    booking_data = pd.read_excel("data_dummy_bookings.xlsx")
    booking_ids = booking_data.index.tolist()
except FileNotFoundError:
    print("data_dummy_bookings.xlsx not found.")
    booking_ids = []

data = []

for index, row in booking_data.iterrows():
    recommended_time = datetime.strptime(row['Recommended Time'], '%H:%M:%S')
    arrival_time = recommended_time + timedelta(minutes=random.randint(-5, 60), seconds=random.randint(0, 59))
    served_time = arrival_time + timedelta(seconds=random.randint(30, 60))
    depart_time = served_time + timedelta(minutes=random.randint(5, 60))
    booking_id = row["id"]

    if (datetime.strptime('07:00:00', '%H:%M:%S').time() <= recommended_time.time() <= datetime.strptime('08:30:00', '%H:%M:%S').time()) and (arrival_time.time() > datetime.strptime('09:00:00', '%H:%M:%S').time()):
        served_time = None
        depart_time = arrival_time + timedelta(minutes=1)

    if (datetime.strptime('11:00:00', '%H:%M:%S').time() <= recommended_time.time() <= datetime.strptime('13:30:00', '%H:%M:%S').time()) and (arrival_time.time() > datetime.strptime('14:00:00', '%H:%M:%S').time()):
        served_time = None
        depart_time = arrival_time + timedelta(minutes=1)

    if (datetime.strptime('17:00:00', '%H:%M:%S').time() <= recommended_time.time() <= datetime.strptime('19:30:00', '%H:%M:%S').time()) and (arrival_time.time() > datetime.strptime('20:00:00', '%H:%M:%S').time()):
        served_time = None
        depart_time = arrival_time + timedelta(minutes=1)

    data.append([arrival_time.time(), served_time.time() if served_time else None, depart_time.time(), booking_id+1])

df = pd.DataFrame(data, columns=['Arrival Time', 'Served Time', 'Depart Time', 'Booking ID'])
df.to_excel('data_dummy_live_booking.xlsx', index=False)

print("Live Booking Generated Successfully")
