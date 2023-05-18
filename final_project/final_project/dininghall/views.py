from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import table_menu
from .forms import MenuForm

# Create your views here.
def dininghall_index(request):
    menu_object = table_menu.objects.all()
    context = {"menu_objects": menu_object}
    return render(request, "dininghall/dininghall_index.html", context)

def add_menu(request):
    submitted = False
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("add_menu?submitted=True")
    else:
        form = MenuForm
        if "submitted" in request.GET:
            submitted = True
    return render(request, "dininghall/add_menu.html", {"form":form, "submitted":submitted})

def edit_menu(request, menu_id):
    menu = table_menu.objects.get(pk=menu_id)
    form = MenuForm(request.POST or None, instance=menu)
    if form.is_valid():
        form.save()
        return redirect('dininghall_index')

    return render(request, 'dininghall/edit_menu.html', 
                  {'menu':menu,
                   'form':form})

def delete_menu(request, menu_id):
    menu = table_menu.objects.get(pk=menu_id)
    menu.delete()
    return redirect('dininghall_index')

