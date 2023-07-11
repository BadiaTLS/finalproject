from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib import messages
from .utils import *

# Create your views here.
def check_sas_role(user):
    return user.role == 'SAS' or user.role == 'sas'

@login_required(login_url='login')
@user_passes_test(check_sas_role, login_url='not_sas')
def sas_index(request):
    user_data = get_all_user()
    class_data = get_all_class()

    context = {
        'user_data':user_data, 
        'class_data':class_data,
        'email':request.user.email,
        }
    return render(request, "sas/sas_index.html", context=context)

@login_required(login_url='login')
@user_passes_test(check_sas_role, login_url='not_sas')
def import_user(request):
    if request.method != 'POST':
        context = {'email':request.user.email,}
        return render(request, 'sas/import_user.html', context=context)

    excel_file = request.FILES['excel_file']

    if not excel_file.name.endswith('.xlsx'):
        messages.error(request, 'Invalid file format. Please upload an Excel file.', extra_tags='error')
        return render(request, 'sas/import_user.html')

    new_users, existing_users = process_excel_file(excel_file)
    update_database(new_users, existing_users)

    messages.success(request, 'Users imported successfully.', extra_tags='success')
    return redirect('sas_index')

@login_required(login_url='login')
@user_passes_test(check_sas_role, login_url='not_sas')
def import_class(request):
    context = {'email':request.user.email,}
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']

        if handle_uploaded_file(excel_file):
            messages.success(request, 'Classes imported successfully.', extra_tags='success')
            return redirect('import_class')
        else:
            messages.error(request, 'Invalid file format. Please upload an Excel file (.xlsx).', extra_tags='error')
            return redirect('import_class')
    else:
        return render(request, 'sas/import_class.html', context=context)


from django.shortcuts import render
from .forms import UploadFileForm

@login_required(login_url='login')
@user_passes_test(check_sas_role, login_url='not_sas')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            success = handle_uploaded_file(file)
            if success:
                messages.success(request, 'Classes imported successfully.', extra_tags='success')
                return render(request, 'sas/upload.html')
            else:
                messages.error(request, 'Invalid file format. Please upload an Excel file (.xlsx).', extra_tags='error')
                return render(request, 'sas/upload.html')
    else:
        form = UploadFileForm()
    return render(request, 'sas/upload.html', {'form': form})

def delete_all_class_view(request):
    if request.method == 'POST':
        # Call the delete_all_class function to delete all data
        delete_all_class()

        # Redirect to a success page
        messages.success(request, 'Classes Delete Success.', extra_tags='success')
        return redirect('sas_index')
    messages.success(request, 'Class Delete Failed.', extra_tags='danger')
    return redirect('sas_index')

def not_sas(request):
    messages.error(request, 'You are not authorized to access different role resources', extra_tags='error')
    return redirect('sas_index')
