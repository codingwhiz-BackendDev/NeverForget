from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth 
from django.http import HttpResponse,JsonResponse
from .models import BirthdayInfo, AdminProfile
from django.core.files.storage import FileSystemStorage
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


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
        
        if BirthdayInfo.objects.filter(community_user_name=community_user_name, phoneNumber=phoneNumber).exists():
            messages.error(request, 'User already exists!!!') 
        else:
        
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
        
            
        
        return HttpResponse(f'{personName} successfully added')

def search_community(request):
    return render(request, 'search_community.html')
 
@login_required(login_url='login')
def community_member(request, pk):
    member = get_object_or_404(BirthdayInfo, pk=pk)

    if request.method == 'POST':
        # Store current phone number
        current_phone = member.phoneNumber
        new_phone = request.POST.get('phoneNumber', '').strip()

        # Check if the new phone is already used by someone else
        if new_phone and new_phone != current_phone:
            if BirthdayInfo.objects.filter(phoneNumber=new_phone).exclude(pk=member.pk).exists():
                messages.warning(request, "This phone number is already used by another member.")
                return render(request, 'community_member.html', {'member': member})

        member.personName = request.POST.get('personName', member.personName)

        birth_date = request.POST.get('birthDate')
        if birth_date:
            member.birthDate = birth_date

        member.email = request.POST.get('email', member.email)
        member.phoneNumber = new_phone if new_phone else current_phone
        member.matric = request.POST.get('matric', member.matric)
        member.department = request.POST.get('department', member.department)

        level = request.POST.get('level')
        member.level = level if level else member.level

        member.gender = request.POST.get('gender', member.gender)
        member.trainingLevel = request.POST.get('trainingLevel', member.trainingLevel)

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
    user = get_object_or_404(User, username=pk)
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

        if BirthdayInfo.objects.filter(community_user_name=community_user_name, phoneNumber=phoneNumber).exists():
            messages.error(request, 'User with this phone number already exists!')
            return redirect('profile', pk=community_user_name.username)

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
            messages.success(request, f"{personName} was successfully added!")
            return redirect('profile', pk=community_user_name.username)

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('form_link', pk=community_user_name.username)

    context = {
        'community_user_name': community_user_name
    }
    return render(request, 'formLink.html', context)


# PWA API Endpoints
@csrf_exempt
@require_http_methods(["POST"])
def push_subscription(request):
    """Handle push notification subscription"""
    try:
        data = json.loads(request.body)
        # Store subscription data (you might want to create a model for this)
        # For now, we'll just return success
        return JsonResponse({'status': 'success', 'message': 'Subscription saved'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def send_birthday_notification(request):
    """Send birthday notification via push"""
    try:
        data = json.loads(request.body)
        # Here you would implement the actual push notification logic
        # For now, we'll just return success
        return JsonResponse({'status': 'success', 'message': 'Notification sent'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def offline_page(request):
    """Serve offline page"""
    return render(request, 'offline.html')


def service_worker(request):
    """Serve service worker with correct content type"""
    response = HttpResponse(open('static/sw.js', 'r').read(), content_type='application/javascript')
    return response


def manifest(request):
    """Serve manifest with correct content type"""
    response = HttpResponse(open('static/manifest.json', 'r').read(), content_type='application/manifest+json')
    return response