from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth 
from django.http import HttpResponse,JsonResponse
from .models import BirthdayInfo, AdminProfile
from django.core.files.storage import FileSystemStorage
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required


def calculate_age(born, ref_date):
    return ref_date.year - born.year - ((ref_date.month, ref_date.day) < (born.month, born.day))

def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def home(request):
    
    user_obj = User.objects.get(username=request.user)
    adminProfile = AdminProfile.objects.get(user=user_obj)
    
    
    today = date.today()
    all_birthdays = BirthdayInfo.objects.filter(community_user_name=request.user)
    number_of_community_members = len(all_birthdays)
    
    todays_birthdays = []
    tomorrows_birthdays = []
    upcoming_birthdays = []

    for b in all_birthdays:
        if b.birthDate:
            bday_this_year = b.birthDate.replace(year=today.year)
            if bday_this_year < today:
                next_bday = bday_this_year.replace(year=today.year + 1)
            else:
                next_bday = bday_this_year

            days_until = (next_bday - today).days
            days_since = (today - bday_this_year).days if bday_this_year < today else None
            age_on_next_bday = calculate_age(b.birthDate, next_bday)

            b.days_until = days_until
            b.days_since = days_since
            b.age_on_next_bday = age_on_next_bday

            if days_until == 0:
                todays_birthdays.append(b)
            elif days_until == 1:
                tomorrows_birthdays.append(b)
            else:
                upcoming_birthdays.append(b)

    # Sort: future birthdays first, then past birthdays (most recent first)
    upcoming_birthdays.sort(key=lambda x: (x.days_until if x.days_until > 0 else 9999 + x.days_since))
    
    # Get only the first 10 upcoming birthdays
    upcoming_birthdays = upcoming_birthdays[:10]
    
    context = {
        'todays_birthdays': todays_birthdays,
        'tomorrows_birthdays': tomorrows_birthdays,
        'upcoming_birthdays': upcoming_birthdays,
        'all_birthdays':all_birthdays,
        'number_of_community_members':number_of_community_members,
        'adminProfile':adminProfile
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
                user_obj = User.objects.get(username=username)
                admin_user = AdminProfile.objects.create(user=user_obj)
                admin_user.save()
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


@login_required(login_url='login')
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
 
@login_required(login_url='login')
def community_member(request, pk):
    member = get_object_or_404(BirthdayInfo, pk=pk)
    if request.method == 'POST':
        member.personName = request.POST.get('personName', member.personName)
        
        # Handle date field safely
        birth_date = request.POST.get('birthDate')
        if birth_date:
            member.birthDate = birth_date
        # else: do not update if empty
        
        member.email = request.POST.get('email', member.email)
        phone = request.POST.get('phoneNumber')
        member.phoneNumber = phone if phone else member.phoneNumber
        member.matric = request.POST.get('matric', member.matric)
        member.department = request.POST.get('department', member.department)
        level = request.POST.get('level')
        member.level = level if level else member.level
        member.gender = request.POST.get('gender', member.gender)
        member.trainingLevel = request.POST.get('trainingLevel', member.trainingLevel)
        # Handle image upload if a new image is provided
        if request.FILES.get('personImage'):
            member.personImage = request.FILES['personImage']
        member.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('community_member', pk=member.pk)
    return render(request, 'community_member.html', {'member': member})
 
@login_required(login_url='login')
def profile(request):
    user_obj = User.objects.get(username=request.user)
    adminProfile = AdminProfile.objects.get(user=user_obj)
    
    all_birthdays = BirthdayInfo.objects.filter(community_user_name=user_obj)
    number_of_community_members = len(all_birthdays) 
    context ={
        'adminProfile':adminProfile,
        'number_of_community_members':number_of_community_members,
    }
    return render(request, 'adminProfile.html', context)


@login_required(login_url='login')
def editAdminProfile(request):
    if request.method == 'POST':
        user = request.user
        community_name = request.POST.get('community_name') 
        phone_number = request.POST.get('phoneNumber')
        birthday = request.POST.get('birthday')
        admin_image = request.FILES.get('profile_image')

        try:
            profile = AdminProfile.objects.get(user=user)
            profile.community_name = community_name
            profile.phone_number = phone_number
            profile.birthday = birthday
            if admin_image:
                profile.adminImage = admin_image
            profile.save()
            return JsonResponse({'message': 'Profile updated successfully.'})
        except AdminProfile.DoesNotExist:
            AdminProfile.objects.create(
                user=user,
                community_name=community_name,
                phone_number=phone_number,
                birthday=birthday,
                adminImage=admin_image,
                email=user.email  # Required field
            )
            return JsonResponse({'message': 'Profile created successfully.'})
    
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def formLink(request, pk):
    user = User.objects.get(username=pk)
    community_user_name = user
    
    if request.method == 'POST':
        personName = request.POST.get('personName')
        birthDate = request.POST.get('birthDate')
        phoneNumber = request.POST.get('phoneNumber')
        email = request.POST.get('email')
        matric = request.POST.get('matric')
        department = request.POST.get('department')
        level = request.POST.get('level')
        gender = request.POST.get('gender')
        trainingLevel = request.POST.get('trainingLevel')
        reminderDays = request.POST.get('reminderDays')
        
        personImage = request.FILES.get('personImage')
        
        try:
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
            
            # For AJAX requests, return JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'{personName} successfully added'})
            
            # For regular form submissions
            messages.success(request, f"{personName} successfully added")
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
    
    # This handles GET requests (when the page is first loaded)
    context = {
        'community_user_name': community_user_name
    }
    return render(request, 'formLink.html', context)  # REMOVED THE COMMA!