from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth 
from django.http import HttpResponse
from .models import BirthdayInfo

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
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def addBirthday(request):
    if request.method == 'POST':
        get_user = request.user
        community_user_name = User.objects.get(username=get_user) 
        
        personName = request.POST['personName']
        birthDate = request.POST['birthDate']
        phoneNumber = request.POST['phoneNumber']
        email =  request.POST['email']
        matric =  request.POST['matric']
        department =  request.POST['department']
        level =  request.POST['level']
        
        personImage = request.FILES.get()
        
        birthdayInfo = BirthdayInfo.objects.create(community_user_name=community_user_name,personName=personName,birthDate=birthDate, phoneNumber=phoneNumber, email=email, matric=matric, department=department,level=level)
        birthdayInfo.save();
        
        messages.success(request, f"{personName} successfully added")
        
        return HttpResponse('Saved')

def search_community(request):
    return render(request, 'search_community.html')
 
def home(request):
    return render(request, 'home.html')
