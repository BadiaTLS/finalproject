from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import MenuForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.db import transaction
from .utils import *

def check_dininghall_role(user):
    return user.role == 'dininghall'

@login_required(login_url='login')
@user_passes_test(check_dininghall_role, login_url='not_dininghall')
def dininghall_index(request):
    menu_objects = get_all_menu_objects()
    context = {"menu_objects": menu_objects}
    return render(request, "dininghall/dininghall_index.html", context)

@login_required(login_url='login')
@user_passes_test(check_dininghall_role, login_url='not_dininghall')
@transaction.atomic
def add_menu(request):
    submitted = False
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            save_menu(form)
            return HttpResponseRedirect("add_menu?submitted=True")
    else:
        form = MenuForm()
        if "submitted" in request.GET:
            submitted = True
    return render(request, "dininghall/add_menu.html", {"form": form, "submitted": submitted})

@login_required(login_url='login')
@user_passes_test(check_dininghall_role, login_url='not_dininghall')
@transaction.atomic
def edit_menu(request, menu_id):
    menu = get_menu_by_id(menu_id)
    form = MenuForm(request.POST or None, instance=menu)
    if form.is_valid():
        update_menu(form)
        return redirect('dininghall_index')
    return render(request, 'dininghall/edit_menu.html', {'menu': menu, 'form': form})

@login_required(login_url='login')
@user_passes_test(check_dininghall_role, login_url='not_dininghall')
@transaction.atomic
def delete_menu(request, menu_id):
    menu = get_menu_by_id(menu_id)
    delete_menu_object(menu)
    return redirect('dininghall_index')

def not_dininghall(request):
    messages.error(request, 'You are not authorized to access dining hall resources. You need the Dining Hall role.')
    return redirect('student_index')
