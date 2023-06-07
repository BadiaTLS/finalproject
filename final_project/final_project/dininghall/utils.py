from .models import table_session, table_time
from datetime import time
import openpyxl

def get_all_session_objects():
    return table_session.objects.all()

def get_time_objects(session_id):
    session = table_session.objects.get(id=session_id)
    return session.table_time_set.all()

def get_session_by_id(session_id):
    return table_session.objects.get(pk=session_id)

def get_time_by_id(time_id):
    return table_time.objects.get(pk=time_id)

def update_session(form_session):
    form_session.save()
    
def delete_session_object(menu_id):
    menu_id.delete()

def delete_time_object(time_id):
    time_id.delete()

def export_data_to_excel(file_path):
    # Create a new Excel workbook
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Write headers
    headers = ["Date", "Name", "Time", "Available", "Limit", "Menu"]
    for col_num, header in enumerate(headers, 1):
        worksheet.cell(row=1, column=col_num, value=header)

    # Fetch data from the models
    sessions = table_session.objects.all()
    for session in sessions:
        times = table_time.objects.filter(session_id=session.id)

        for time in times:
            # Get the session data
            date = session.date
            name = session.get_name_display()
            menu = session.menu

            # Get the time data
            time_value = time.time
            available = time.available_seat
            limit = time.seat_limit

            # Write data to Excel
            row_data = [date, name, time_value, available, limit, menu]
            row_num = worksheet.max_row + 1
            for col_num, value in enumerate(row_data, 1):
                worksheet.cell(row=row_num, column=col_num, value=value)

    # Save the workbook
    workbook.save(file_path)

def save_session_and_times(form_session, form_time):
    session = form_session.save()

    if session.name == "Breakfast":
        times = [
            time(7, 0),
            time(7, 30),
            time(8, 0),
            time(8, 30),
            time(9, 0),
        ]
    elif session.name == "Lunch":
        times = [
            time(11, 0),
            time(11, 30),
            time(12, 0),
            time(12, 30),
            time(13, 0),
            time(13, 30),
        ]
    elif session.name == "Dinner":
        times = [
            time(17, 0),
            time(17, 30),
            time(18, 0),
            time(18, 30),
            time(19, 0),
            time(19, 30),
        ]
    else:
        times = []

    for time_value in times:
        table_time.objects.create(
            time=time_value,
            session_id=session,
            seat_limit=form_time.cleaned_data["seat_limit"],
        )


