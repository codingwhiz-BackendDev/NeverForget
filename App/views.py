from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth 

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        password2 = request.POST['password2'].strip()

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email Already Exists')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username Already Exists')
            else:
                # Create user using Django's create_user method
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.save()
                messages.success(request, 'Successfully Registered')
                return redirect('login')
        else:
            messages.error(request, 'Password does not match')

    return render(request, 'register.html')

def login(request):
    """User login view"""
    if request.method == 'POST':
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()

        # Authenticate user
        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Successfully logged in as {user}")
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def search_community(request):
    return render(request, 'search_community.html')
 
