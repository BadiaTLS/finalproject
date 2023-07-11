import openpyxl
import pandas as pd
from datetime import time
from final_project.accounts.models import CustomUser
from django.contrib.auth.hashers import make_password
from .models import table_classes, Attendee

def get_all_user():
    return CustomUser.objects.all()

def get_all_class():
    return table_classes.objects.all()

def process_excel_file(excel_file):
    workbook = openpyxl.load_workbook(excel_file)
    worksheet = workbook.active

    new_users = []
    existing_users = []

    # Fetch all existing users from the database and store them in a dictionary
    existing_users_dict = {user.email: user for user in CustomUser.objects.all()}

    for row in worksheet.iter_rows(min_row=2, values_only=True):
        user_id, name, email, role, gender, major = row
        print(f"User {user_id} checked")

        # Check if user with the same email exists
        user = existing_users_dict.get(email)
        if user:
            # User already exists, update the fields
            user.username = user_id
            user.name = name
            user.role = role
            user.gender = gender
            user.major = major
            existing_users.append(user)
        else:
            hashed_password = make_password(user_id, hasher='pbkdf2_sha256')

            # Create a new user
            new_user = CustomUser(
                username=user_id,
                password=hashed_password,
                email=email,
                name=name,
                role=role,
                gender = gender,
                major = major,
            )
            new_users.append(new_user)

    return new_users, existing_users


def update_database(new_users, existing_users):
    # Create new users and update existing users in a single database query
    CustomUser.objects.bulk_create(new_users)
    CustomUser.objects.bulk_update(existing_users, ['username', 'name', 'role', 'gender', 'major'])

def handle_uploaded_file(file):
    # Read the contents of the uploaded file into a DataFrame
    df = pd.read_excel(file)

    # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        # Get or create a table_classes object for each row
        class_obj, created = table_classes.objects.get_or_create(
            class_code=row['class_code'],
            defaults={
                'class_name': row['class_name'],
                'class_day': row['class_day'],
                'class_start_time': row['class_start_time'],
                'class_end_time': row['class_end_time']
            }
        )

        # Update the fields of the table_classes object if it already exists
        if not created:
            class_obj.class_name = row['class_name']
            class_obj.class_day = row['class_day']
            class_obj.class_start_time = row['class_start_time']
            class_obj.class_end_time = row['class_end_time']
            class_obj.save()

        # Split the attendees field into a list of email addresses
        attendees = row['attendees'].split(', ')

        # Clear the existing attendees from the table_classes object
        class_obj.attendees.clear()

        # Iterate over the email addresses
        for email in attendees:
            # Get or create an Attendee object for each email address
            attendee, created = Attendee.objects.get_or_create(email=email)

            # Add the attendee to the table_classes object
            class_obj.attendees.add(attendee)

    return True

def delete_all_class():
    # Delete all table_classes objects
    table_classes.objects.all().delete()

    # Delete all Attendee objects
    Attendee.objects.all().delete()