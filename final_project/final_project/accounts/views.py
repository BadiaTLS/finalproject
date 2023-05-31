from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.role == 'student':
                login(request, user)
                return redirect('/student')
            elif user.role == 'dininghall':
                login(request, user)
                return redirect('/dininghall')
        else:
            messages.success(request, ("There was an error, try again"))
            return redirect('login')
    else:
        return render(request, 'accounts/login.html', {})
    
def logout_user(request):
    logout(request)
    return redirect('login')