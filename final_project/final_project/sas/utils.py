import openpyxl
import pandas as pd
from datetime import time
from final_project.accounts.models import CustomUser
from django.contrib.auth.hashers import make_password
from .models import table_classes, Attendee
from django.db import transaction

def get_all_user():
    return CustomUser.objects.all()

def get_all_class():
    return table_classes.objects.all()

# IMPORT USERS
def process_excel_file(excel_file):
    workbook = openpyxl.load_workbook(excel_file)
    worksheet = workbook.active

    new_users = []
    existing_users = []

    # Fetch all existing users from the database and store them in a dictionary
    existing_users_dict = {user.email: user for user in CustomUser.objects.all()}

    for row in worksheet.iter_rows(min_row=2, values_only=True):
        user_id = row[0]
        name = row[1]
        email = row[2]
        role = row[3]

        # Check if user with the same email exists
        user = existing_users_dict.get(email)
        if user:
            # User already exists, update the fields
            user.username = user_id
            user.name = name
            user.role = role
            existing_users.append(user)
        else:
            hashed_password = make_password(user_id, hasher='pbkdf2_sha256')

            # Create a new user
            new_user = CustomUser(username=user_id, password=hashed_password, email=email)
            new_user.name = name
            new_user.role = role
            new_users.append(new_user)

    return new_users, existing_users


def update_database(new_users, existing_users):
    # Create new users and update existing users in a single database query
    CustomUser.objects.bulk_create(new_users)
    CustomUser.objects.bulk_update(existing_users, ['username', 'name', 'role'])

# IMPORT CLASSES
# def handle_uploaded_file(excel_file):
#     # Check if file is an Excel file
#     if not excel_file.name.endswith(".xlsx"):
#         return False

#     # Read data from Excel file
#     data = pd.read_excel(excel_file)

#     # Iterate over rows of data
#     for index, row in data.iterrows():
#         # Get data from row
#         class_code = row["class_code"]
#         class_name = row["class_name"]
#         class_day = row["class_day"].lower()
#         class_start_time = time(hour=int(row["class_start_time"].split(":")[0]), minute=int(row["class_start_time"].split(":")[1]))
#         class_end_time = time(hour=int(row["class_end_time"].split(":")[0]), minute=int(row["class_end_time"].split(":")[1]))
#         attendees = row["attendees"].split(", ")

#         # Create Attendee objects
#         for email in attendees:
#             Attendee.objects.get_or_create(email=email)

#         # Create table_classes object
#         table_class = table_classes.objects.create(
#             class_code=class_code,
#             class_name=class_name,
#             class_day=class_day,
#             class_start_time=class_start_time,
#             class_end_time=class_end_time
#         )

#         # Add attendees to table_classes object
#         for email in attendees:
#             attendee = Attendee.objects.get(email=email)
#             table_class.attendees.add(attendee)

#     return True

def handle_uploaded_file(excel_file):
    # Check if file is an Excel file
    if not excel_file.name.endswith(".xlsx"):
        return False

    # Read data from Excel file
    data = pd.read_excel(excel_file)

    # Get all existing Attendee objects
    existing_attendees = Attendee.objects.all()
    existing_attendees_emails = [attendee.email for attendee in existing_attendees]

    # Create a list to store new Attendee objects
    new_attendees = []

    # Iterate over rows of data
    for index, row in data.iterrows():
        # Get data from row
        class_code = row["class_code"]
        class_name = row["class_name"]
        class_day = row["class_day"].lower()
        class_start_time = time(hour=int(row["class_start_time"].split(":")[0]), minute=int(row["class_start_time"].split(":")[1]))
        class_end_time = time(hour=int(row["class_end_time"].split(":")[0]), minute=int(row["class_end_time"].split(":")[1]))
        attendees = row["attendees"].split(", ")

        # Create new Attendee objects
        for email in attendees:
            if email not in existing_attendees_emails:
                new_attendees.append(Attendee(email=email))

        # Create table_classes object
        table_class = table_classes.objects.create(
            class_code=class_code,
            class_name=class_name,
            class_day=class_day,
            class_start_time=class_start_time,
            class_end_time=class_end_time
        )

        # Add attendees to table_classes object
        for email in attendees:
            attendee = next((attendee for attendee in existing_attendees if attendee.email == email), None)
            if attendee is None:
                attendee = next((attendee for attendee in new_attendees if attendee.email == email), None)
            table_class.attendees.add(attendee)

    # Create new Attendee objects in database
    Attendee.objects.bulk_create(new_attendees)

    return True
