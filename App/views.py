from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth 
from django.http import HttpResponse
from .models import BirthdayInfo
from django.core.files.storage import FileSystemStorage
from datetime import date, timedelta

def index(request):
    return render(request, 'index.html')

def home(request):
    today = date.today()
    tomorrow = today + timedelta(days=1)

    all_birthdays = BirthdayInfo.objects.filter(community_user_name=request.user)
    
    print(f"-----------------------------------------")
    print(f"Checking birthdays for user: {request.user}")
    print(f"Today's date: {today}")
    print(f"Found {all_birthdays.count()} total birthdays for this user.")

    todays_birthdays = []
    tomorrows_birthdays = []
    upcoming_birthdays = []

    for b in all_birthdays:
        if b.birthDate:
            bday_this_year = b.birthDate.replace(year=today.year)
            
            print(f"Processing {b.personName}'s birthday on {b.birthDate} (this year: {bday_this_year})")

            if bday_this_year == today:
                todays_birthdays.append(b)
                print(f"  -> Added to TODAY'S birthdays")
            elif bday_this_year == tomorrow:
                tomorrows_birthdays.append(b)
                print(f"  -> Added to TOMORROW'S birthdays")
            elif today < bday_this_year <= today + timedelta(days=7):
                upcoming_birthdays.append(b)
                print(f"  -> Added to UPCOMING birthdays")
    
    print(f"Final list - Today: {[p.personName for p in todays_birthdays]}")
    print(f"Final list - Tomorrow: {[p.personName for p in tomorrows_birthdays]}")
    print(f"Final list - Upcoming: {[p.personName for p in upcoming_birthdays]}")
    print(f"-----------------------------------------")

    context = {
        'todays_birthdays': todays_birthdays,
        'tomorrows_birthdays': tomorrows_birthdays,
        'upcoming_birthdays': upcoming_birthdays,
    }
    return render(request, 'home.html', context)

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
        
        personName = request.POST.get('personName')
        birthDate = request.POST.get('birthDate')
        phoneNumber = request.POST.get('phoneNumber')
        email =  request.POST.get('email')
        matric =  request.POST.get('matric')
        department =  request.POST.get('department')
        level =  request.POST.get('level')
        gender = request.POST.get('gender')
        trainingLevel = request.POST.get('trainingLevel')
        reminderDays = request.POST.get('reminderDays')
        
        personImage = request.FILES.get('personImage')
        
        BirthdayInfo.objects.create(
            community_user_name=community_user_name,
            personName=personName,
            birthDate=birthDate, 
            phoneNumber=phoneNumber, 
            email=email, 
            matric=matric, 
            department=department,
            level=level, 
            personImage=personImage,
            gender=gender,
            trainingLevel=trainingLevel,
            reminderDays=reminderDays
            )
        
        messages.success(request, f"{personName} successfully added")
        
        return HttpResponse(f'{personName} successfully added')

def search_community(request):
    return render(request, 'search_community.html')
 

