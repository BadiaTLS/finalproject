from django.shortcuts import render, redirect
from .forms import SessionForm, TimeForm
from django.contrib import messages
from django.db import transaction
from .utils import *
from datetime import time

def dininghall_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'dininghall':
            return redirect('not_dininghall')
        return view_func(request, *args, **kwargs)
    return wrapped_view

@dininghall_required
def edit_menu_table(request):
    session_objects = fetch_all_session_objects()
    session_ids = [session.id for session in session_objects]
    time_objects = []

    for session_id in session_ids:
        time_objects.append((session_id, fetch_time_objects(session_id)))

    context = {"session_objects": session_objects, "time_objects": time_objects}
    context['email'] = request.user.email
    return render(request, "dininghall/edit_menu_table.html", context)

@dininghall_required
def dininghall_home_page(request):
    context = {}
    context['email'] = request.user.email
    return render(request, "dininghall/dininghall_home_page.html", context)

@dininghall_required
@transaction.atomic
def add_session(request):
    submitted = False
    if request.method == "POST":
        form_session = SessionForm(request.POST)
        form_time = TimeForm(request.POST)
        if form_session.is_valid() and form_time.is_valid():
            save_session_and_times(form_session, form_time)
            messages.success(request, "Add New Session Successfully", extra_tags='success')
            return redirect("edit_menu_table")
    else:
        form_session = SessionForm()
        form_time = TimeForm()
        if "submitted" in request.GET:
            submitted = True
    context = {"form_session": form_session, "form_time": form_time, "submitted": submitted}
    context['email'] = request.user.email
    return render(request, "dininghall/add_menu.html", context)

@dininghall_required
@transaction.atomic
def edit_session(request, session_id):
    session = get_session_by_id(session_id)
    form = SessionForm(request.POST or None, instance=session)
    if form.is_valid():
        update_session_limit(form)
        messages.success(request, "Edit Session Successfully", extra_tags='success')
        return redirect('edit_menu_table')
    
    context = {'menu': session, 'form': form}
    context['email'] = request.user.email
    return render(request, 'dininghall/edit_menu_manual.html', context)

@dininghall_required
@transaction.atomic
def delete_session(request, session_id):
    session = get_session_by_id(session_id)
    delete_session_object(session)
    messages.success(request, "Delete Menu Succesfully", extra_tags='success')
    return redirect('edit_menu_table')

@dininghall_required
@transaction.atomic
def edit_time(request, time_id):
    time = get_time_by_id(time_id)
    form = TimeForm(request.POST or None, instance=time)
    if form.is_valid():
        limit_value = request.POST.get("seat_limit")
        update_session_available_seat(time_id=time_id, limit_after=int(limit_value))
        if not update_session_available_seat:
            messages.success(request, "Edit Time Failed", extra_tags='danger')
            return redirect('edit_menu_table')    
        messages.success(request, "Edit Time Successfully", extra_tags='success')
        return redirect('edit_menu_table')
    context = {'time_objects': time, 'form': form}
    context['email'] = request.user.email
    return render(request, 'dininghall/edit_menu_manual.html', context )

@dininghall_required
@transaction.atomic
def delete_time(request, time_id):
    session = get_time_by_id(time_id)
    delete_time_object(session)
    messages.success(request, "Delete Time Succesfully", extra_tags='success')
    return redirect('edit_menu_table')

@dininghall_required
def upload_menu_file(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']

        if excel_file.name.endswith('.xlsx'):
            try:
                workbook = openpyxl.load_workbook(excel_file)
                worksheet = workbook.active
            except Exception as e:
                messages.error(request, f'Error reading Excel file: {e}', extra_tags='error')
                return redirect('upload_menu_file')

            # validate required columns
            required_columns = ['Date', 'Name', 'Menu', 'Seat Limit']
            headers = [cell.value for cell in worksheet[1]]
            missing_columns = [col for col in required_columns if col not in headers]
            if missing_columns:
                messages.error(request, f'Missing required columns: {", ".join(missing_columns)}', extra_tags='error')
                return redirect('upload_menu_file')

            with transaction.atomic():
                for row in worksheet.iter_rows(min_row=2, values_only=True):
                    date = row[0]
                    name = row[1]
                    menu = row[2]
                    seat_limit = row[3]

                    session, created = table_session.objects.update_or_create(
                        date=date,
                        name=name,
                        defaults={
                            'menu': menu,
                        }
                    )

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

                    # retrieve existing table_time objects for this session
                    existing_times = table_time.objects.filter(session_id=session)

                    # update or create table_time objects
                    for t in times:
                        table_t, created = table_time.objects.update_or_create(
                            session_id=session,
                            time=t,
                            defaults={
                                'seat_limit': seat_limit,
                                'available_seat': seat_limit,
                            }
                        )

            messages.success(request, 'Sessions and times imported successfully.', extra_tags='success')
            return redirect('edit_menu_table')
        else:
            messages.error(request, 'Invalid file format. Please upload an Excel file (.xlsx).', extra_tags='error')
            return redirect('upload_menu_file')
    else:
        context = {'email': request.user.email}
        return render(request, 'dininghall/upload_menu_file.html', context)

@dininghall_required
def download_report(request):
    context = {}
    context = {'email': request.user.email}
    if request.method == 'POST':
        # Star Date and End Date is String
        start_date = request.POST.get('start_range')
        end_date = request.POST.get('end_range')
        if not validate_dates(start_date, end_date):
            messages.success(request, "We regret to inform you that the data download has failed due to incorrect date input. Please enter the date correctly to proceed. Thank you for your attention to this matter.", extra_tags='danger')
            return render(request, 'dininghall/download_report.html', context=context)
        _,  start_date, end_date = validate_dates(start_date, end_date)
        file_path = f"Order Report from {start_date} to {end_date}.doc"
        messages.success(request, "Download Success", extra_tags='success')
        # return render(request, 'dininghall/download_report.html', context=context)
        return download_report_doc(start_date=start_date, end_date=end_date, filename=file_path)
    else:
        return render(request, 'dininghall/download_report.html', context=context)

def not_dininghall(request):
    messages.error(request, 'You are not authorized to access dining hall resources. You need the Dining Hall role.', extra_tags='error')
    return redirect('student_index')
