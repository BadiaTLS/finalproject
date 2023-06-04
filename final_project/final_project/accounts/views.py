from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.role == 'student' or user.role == 'dininghall':
                login(request, user)
                return redirect('/' + user.role)
        else:
            messages.success(request, "There was an error, try again")
    
    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')
