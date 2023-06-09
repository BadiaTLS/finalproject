from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if is_valid_user_role(user.role):
                login(request, user)
                messages.success(request, "You have successfully logged in.", extra_tags='success')
                return redirect('/' + user.role)
            else:
                messages.error(request, "Invalid email or password. Please try again.", extra_tags='error')
        else:
            messages.error(request, "Invalid email or password. Please try again.", extra_tags='error')
    
    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def is_valid_user_role(role):
    return role in ['student', 'dininghall', 'sas']
