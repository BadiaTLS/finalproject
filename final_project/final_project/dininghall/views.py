from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import table_menu
from .forms import MenuForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.db import transaction

@login_required(login_url='login')
@user_passes_test(lambda u: u.role == 'dininghall', login_url='not_dininghall')
def dininghall_index(request):
    menu_objects = table_menu.objects.all()
    context = {"menu_objects": menu_objects}
    return render(request, "dininghall/dininghall_index.html", context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.role == 'dininghall', login_url='not_dininghall')
@transaction.atomic
def add_menu(request):
    submitted = False
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("add_menu?submitted=True")
    else:
        form = MenuForm()
        if "submitted" in request.GET:
            submitted = True
    return render(request, "dininghall/add_menu.html", {"form": form, "submitted": submitted})

@login_required(login_url='login')
@user_passes_test(lambda u: u.role == 'dininghall', login_url='not_dininghall')
@transaction.atomic
def edit_menu(request, menu_id):
    menu = table_menu.objects.get(pk=menu_id)
    form = MenuForm(request.POST or None, instance=menu)
    if form.is_valid():
        form.save()
        return redirect('dininghall_index')

    return render(request, 'dininghall/edit_menu.html', {'menu': menu, 'form': form})

@login_required(login_url='login')
@user_passes_test(lambda u: u.role == 'dininghall', login_url='not_dininghall')
@transaction.atomic
def delete_menu(request, menu_id):
    menu = table_menu.objects.get(pk=menu_id)
    menu.delete()
    return redirect('dininghall_index')

def not_dininghall(request):
    messages.error(request, 'You are not authorized to access dining hall resources. You need the Dining Hall role.')
    return redirect('student_index')
