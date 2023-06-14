from django.shortcuts import render, redirect
from .forms import SessionForm, TimeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.db import transaction
from .utils import *
from datetime import time

def check_dininghall_role(user):
    return user.role == 'dininghall'

@login_required(login_url='login')
@user_passes_test(check_dininghall_role, login_url='not_dininghall')
def dininghall_index(request):
    session_objects = fetch_all_session_objects()
    session_ids = [session.id for session in session_objects]
    time_objects = []

    for session_id in session_ids:
        time_objects.append((session_id, fetch_time_objects(session_id)))

    context = {"session_objects": session_objects, "time_objects": time_objects}
    return render(request, "dininghall/dininghall_index.html", context)


@login_required(login_url='login')
@user_passes_test(check_dininghall_role, login_url='not_dininghall')
@transaction.atomic
def add_session(request):
    submitted = False
    if request.method == "POST":
        form_session = SessionForm(request.POST)
        form_time = TimeForm(request.POST)
        if form_session.is_valid() and form_time.is_valid():
            save_session_and_times(form_session, form_time)
            messages.success(request, "Add New Session Successfully", extra_tags='success')
            return redirect("dininghall_index")
    else:
        form_session = SessionForm()
        form_time = TimeForm()
        if "submitted" in request.GET:
            submitted = True
    return render(request, "dininghall/add_menu.html", {"form_session": form_session, "form_time": form_time, "submitted": submitted})

@login_required(login_url='login')
@user_passes_test(check_dininghall_role, login_url='not_dininghall')
@transaction.atomic
def edit_session(request, session_id):
    session = get_session_by_id(session_id)
    form = SessionForm(request.POST or None, instance=session)
    if form.is_valid():
        update_session(form)
        messages.success(request, "Edit Session Successfully", extra_tags='success')
        return redirect('dininghall_index')
    return render(request, 'dininghall/edit_menu.html', {'menu': session, 'form': form})

@login_required(login_url='login')
@user_passes_test(check_dininghall_role, login_url='not_dininghall')
@transaction.atomic
def delete_session(request, session_id):
    session = get_session_by_id(session_id)
    delete_session_object(session)
    messages.success(request, "Delete Menu Succesfully", extra_tags='success')
    return redirect('dininghall_index')

@login_required(login_url='login')
@user_passes_test(check_dininghall_role, login_url='not_dininghall')
@transaction.atomic
def edit_time(request, time_id):
    time = get_time_by_id(time_id)
    form = TimeForm(request.POST or None, instance=time)
    if form.is_valid():
        update_session(form)
        messages.success(request, "Edit Time Successfully", extra_tags='success')
        return redirect('dininghall_index')
    return render(request, 'dininghall/edit_menu.html', {'time_objects': time, 'form': form})

@login_required(login_url='login')
@user_passes_test(check_dininghall_role, login_url='not_dininghall')
@transaction.atomic
def delete_time(request, time_id):
    session = get_time_by_id(time_id)
    delete_time_object(session)
    messages.success(request, "Delete Time Succesfully", extra_tags='success')
    return redirect('dininghall_index')

@login_required(login_url='login')
@user_passes_test(check_dininghall_role, login_url='not_dininghall')
def export_order_record(request):
    file_path = "order_record.xlsx"
    export_data_to_excel(file_path)
    messages.success(request, "Export Data Succesfully", extra_tags='success')
    return download_file_response(file_path)

@login_required(login_url='login')
@user_passes_test(check_dininghall_role, login_url='not_dininghall')
def import_session(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']

        if excel_file.name.endswith('.xlsx'):
            workbook = openpyxl.load_workbook(excel_file)
            worksheet = workbook.active

            for row in worksheet.iter_rows(min_row=2, values_only=True):
                date = row[0]
                name = row[1]
                menu = row[2]
                seat_limit = row[3]  # Retrieve the seat_limit value from the Excel file

                # Retrieve or create the table_session instance
                session, _ = table_session.objects.get_or_create(
                    date=date,
                    name=name,
                    defaults={
                        'menu': menu,
                    }
                )

                # Add rows in table_time based on session name
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

                for t in times:
                    # Create table_time instance for each time
                    table_time.objects.create(
                        time=t,
                        session_id=session,
                        seat_limit=seat_limit,  # Set the seat_limit value from the Excel file
                        available_seat=None,  # Set the appropriate available seat value
                    )

            messages.success(request, 'Sessions and times imported successfully.', extra_tags='success')
            return redirect('dininghall_index')
        else:
            messages.error(request, 'Invalid file format. Please upload an Excel file (.xlsx).', extra_tags='error')
            return redirect('import_session')
    else:
        return render(request, 'dininghall/import_session.html')

def not_dininghall(request):
    messages.error(request, 'You are not authorized to access dining hall resources. You need the Dining Hall role.', extra_tags='error')
    return redirect('student_index')
