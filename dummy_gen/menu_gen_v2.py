import pandas as pd
from datetime import date, timedelta
import random

start_date = date(2023, 5, 1)
end_date = date(2023, 7, 30)
delta = timedelta(days=1)

breakfast_menu = ['Bubur Ayam + Roti Bakar', 'Bubur Kacang Hijau + Roti Canai', 'Oatmeal + Granola', 'Nasi Goreng + Telur Mata Sapi', 'Nasi Kuning + Ayam Goreng', 'Nasi Uduk + Sambal Goreng', 'Lontong Sayur + Kerupuk']
lunch_menu = ['Nasi Campur + Sate Ayam', 'Nasi Padang + Rendang', 'Nasi Goreng + Bakso', 'Nasi Kuning + Pangsit', 'Nasi Uduk + Kentang Goreng', 'Nasi Putih + Ayam Bakar', 'Nasi Putih + Sambal Goreng', 'Gado-gado + Lontong']
dinner_menu = ['Daging Sapi Bakar + Nasi Putih', 'Daging Sapi Goreng + Nasi Putih', 'Ikan Bakar + Nasi Putih', 'Ikan Goreng + Nasi Putih', 'Sayur Asem + Nasi Putih', 'Sayur Lodeh + Nasi Putih', 'Ayam Bakar + Nasi Putih + Sambal', 'Rendang + Nasi Putih']

data = []
while start_date <= end_date:
    if start_date.weekday() not in [5, 6]:  # Skip Saturday (5) and Sunday (0)
        data.append([start_date, 'Breakfast', random.choice(breakfast_menu), 5])
        data.append([start_date, 'Lunch', random.choice(lunch_menu), 5])
        data.append([start_date, 'Dinner', random.choice(dinner_menu), 5])
    start_date += delta

df = pd.DataFrame(data, columns=['Date', 'Name', 'Menu', 'Seat Limit'])
df.to_excel('data_dummy_session.xlsx', index=False)

print("Session Generated Successfully")
