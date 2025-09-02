from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth 
from django.http import HttpResponse, JsonResponse
from .models import BirthdayInfo, AdminProfile, PushSubscription, NotificationPreference, NotificationLog 
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone 
from django.conf import settings
import re
from .utils.vapid_helper import get_vapid_public_key_base64url 
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import base64

def calculate_age(born, ref_date):
    return ref_date.year - born.year - ((ref_date.month, ref_date.day) < (born.month, born.day))


def send_push_notification_to_user(user, title, message, notification_type='birthday'):
    """
    Send push notification to a specific user using pywebpush with proper VAPID key handling
    """
    try:
        from pywebpush import webpush, WebPushException
        
        # Get user's active subscriptions
        subscriptions = PushSubscription.objects.filter(user=user, is_active=True)
        
        if not subscriptions.exists():
            return False, "No active subscriptions found"
        
        vapid_private_key = getattr(settings, 'VAPID_PRIVATE_KEY', None)
        vapid_claims = getattr(settings, 'VAPID_CLAIMS', {
            'sub': 'mailto:admin@neverforget.com'
        })
        
        if not vapid_private_key or vapid_private_key == 'YOUR_VAPID_PRIVATE_KEY_HERE':
            return False, "VAPID_PRIVATE_KEY not configured in settings"
        
        try:
            # Clean and process the private key
            vapid_private_key_clean = vapid_private_key.strip()
            
            # Validate the private key format by loading it
            try:
                private_key_obj = serialization.load_pem_private_key(
                    vapid_private_key_clean.encode('utf-8'),
                    password=None,
                )
                # Convert back to PEM format to ensure it's properly formatted
                vapid_private_key_clean = private_key_obj.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ).decode('utf-8')
            except Exception as key_error:
                return False, f"Invalid VAPID private key format: {str(key_error)}"
            
            # Log the notification attempt
            notification_log = NotificationLog.objects.create(
                user=user,
                notification_type=notification_type,
                title=title,
                message=message,
                status='pending'
            )
            
            success_count = 0
            for subscription in subscriptions:
                try:
                    # Prepare subscription info for pywebpush
                    subscription_info = {
                        'endpoint': subscription.endpoint,
                        'keys': {
                            'p256dh': subscription.p256dh_key,
                            'auth': subscription.auth_key
                        }
                    }
                    
                    # Prepare notification data
                    notification_data = {
                        'title': title,
                        'message': message,
                        'icon': '/static/icons/icon-192x192.png',
                        'badge': '/static/icons/icon-192x192.png',
                        'tag': 'birthday-notification',
                        'data': {
                            'url': '/home',
                            'type': 'birthday'
                        }
                    }
                    
                    response = webpush(
                        subscription_info=subscription_info,
                        data=json.dumps(notification_data),
                        vapid_private_key=vapid_private_key_clean,
                        vapid_claims=vapid_claims
                    )
                    
                    if response.status_code in [200, 201]:
                        success_count += 1
                        
                except WebPushException as e:
                    error_msg = str(e)
                    print(f"WebPush error for subscription {subscription.id}: {error_msg}")
                    
                    # Mark subscription as inactive if it's invalid
                    if any(code in error_msg for code in ['410', '404', '400']):
                        subscription.is_active = False
                        subscription.save()
                        print(f"Marked subscription {subscription.id} as inactive due to error: {error_msg}")
                        
                except Exception as e:
                    print(f"Error sending to subscription {subscription.id}: {str(e)}")
            
            # Update notification log
            if success_count > 0:
                notification_log.status = 'sent'
                notification_log.delivered_at = timezone.now()
                notification_log.save()
                return True, f"Notification sent successfully to {success_count} device(s)"
            else:
                notification_log.status = 'failed'
                notification_log.error_message = 'No successful deliveries'
                notification_log.save()
                return False, "No successful deliveries"
                
        except Exception as vapid_error:
            return False, f"Failed to process VAPID private key: {str(vapid_error)}"
        
    except ImportError:
        return False, "Required libraries not installed. Run: pip install pywebpush py-vapid"
    except Exception as e:
        return False, str(e)

def index(request):
    return render(request, 'index.html')

def get_vapid_public_key_view(request):
    """API endpoint to serve the VAPID public key in the correct format"""
    try:
        # Load the PEM public key
        public_key_pem = settings.VAPID_PUBLIC_KEY.encode('utf-8')
        
        # Parse the PEM key
        public_key = serialization.load_pem_public_key(public_key_pem)
        
        # Get the raw public key bytes (uncompressed point format)
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        
        # Convert to base64url format (what browsers expect)
        public_key_base64url = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8').rstrip('=')
        
        return JsonResponse({
            'success': True,
            'public_key': public_key_base64url
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

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

    if todays_birthdays:
        # Check if we've already sent notifications today to avoid spam
        today_logs = NotificationLog.objects.filter(
            user=request.user,
            notification_type='birthday',
            sent_at__date=today,
            status='sent'
        )
        
        # Get names of people we've already notified today
        already_notified = [log.title.replace('🎉 Birthday Today: ', '') for log in today_logs]
        
        # Send notifications for birthdays we haven't notified about today
        for birthday in todays_birthdays:
            if birthday.personName not in already_notified:
                title = f"🎉 Birthday Today: {birthday.personName}"
                message = f"It's {birthday.personName}'s birthday today! Don't forget to celebrate! 🎂"
                
                # Send push notification
                success, msg = send_push_notification_to_user(
                    request.user,
                    title,
                    message,
                    'birthday'
                )
                
                # Log the attempt (success or failure)
                if not success:
                    print(f"Failed to send birthday notification for {birthday.personName}: {msg}")

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
        'adminProfile':adminProfile,
       
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
    """
    Handle push notification subscription from PWA
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        
        # Extract subscription data
        endpoint = data.get('endpoint')
        keys = data.get('keys', {})
        p256dh = keys.get('p256dh')
        auth = keys.get('auth')
        
        if not all([endpoint, p256dh, auth]):
            return JsonResponse({'error': 'Invalid subscription data'}, status=400)
        
        # Create or update subscription
        subscription, created = PushSubscription.objects.update_or_create(
            user=request.user,
            endpoint=endpoint,
            defaults={
                'p256dh_key': p256dh,
                'auth_key': auth,
                'is_active': True
            }
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Subscription saved successfully',
            'created': created
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def send_birthday_notification(request):
    """Send birthday notification via push"""
    try:
        data = json.loads(request.body)
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)
        
        # Extract notification data
        birthday_person = data.get('person_name')
        birthday_date = data.get('birthday_date')
        notification_type = data.get('type', 'birthday')
        
        if not birthday_person:
            return JsonResponse({'status': 'error', 'message': 'Missing birthday person name'}, status=400)
        
        # Get user's notification preferences
        try:
            preferences = NotificationPreference.objects.get(user=request.user)
            if not preferences.birthday_notifications:
                return JsonResponse({'status': 'error', 'message': 'Birthday notifications disabled'}, status=400)
        except NotificationPreference.DoesNotExist:
            # Create default preferences if they don't exist
            preferences = NotificationPreference.objects.create(user=request.user)
        
        # Log the notification attempt
        notification_log = NotificationLog.objects.create(
            user=request.user,
            notification_type=notification_type,
            title=f"Birthday: {birthday_person}",
            message=f"It's {birthday_person}'s birthday today! 🎉",
            status='pending'
        )
        
        # Here you would implement the actual push notification sending
        # For now, we'll simulate success
        notification_log.status = 'sent'
        notification_log.save()
        
        return JsonResponse({
            'status': 'success', 
            'message': f'Birthday notification for {birthday_person} logged successfully'
        })
        
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


@login_required
def notification_preferences(request):
    """Manage notification preferences"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Get or create preferences
            preferences, created = NotificationPreference.objects.get_or_create(
                user=request.user,
                defaults={
                    'birthday_notifications': True,
                    'reminder_days': 1,
                    'notification_time': '09:00',
                    'email_notifications': True,
                    'push_notifications': True
                }
            )
            
            # Update preferences
            preferences.birthday_notifications = data.get('birthday_notifications', True)
            preferences.reminder_days = data.get('reminder_days', 1)
            preferences.notification_time = data.get('notification_time', '09:00')
            preferences.email_notifications = data.get('email_notifications', True)
            preferences.push_notifications = data.get('push_notifications', True)
            preferences.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Notification preferences updated successfully'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    # GET request - return current preferences
    try:
        preferences = NotificationPreference.objects.get(user=request.user)
        data = {
            'birthday_notifications': preferences.birthday_notifications,
            'reminder_days': preferences.reminder_days,
            'notification_time': preferences.notification_time.strftime('%H:%M'),
            'email_notifications': preferences.email_notifications,
            'push_notifications': preferences.push_notifications
        }
    except NotificationPreference.DoesNotExist:
        data = {
            'birthday_notifications': True,
            'reminder_days': 1,
            'notification_time': '09:00',
            'email_notifications': True,
            'push_notifications': True
        }
    
    return JsonResponse({'status': 'success', 'data': data}) 


@login_required
def notification_logs(request):
    """Get user's notification logs"""
    logs = NotificationLog.objects.filter(user=request.user).order_by('-sent_at')[:50]
    
    log_data = []
    for log in logs:
        log_data.append({
            'id': log.id,
            'type': log.notification_type,
            'title': log.title,
            'message': log.message,
            'status': log.status,
            'sent_at': log.sent_at.strftime('%Y-%m-%d %H:%M:%S'),
            'delivered_at': log.delivered_at.strftime('%Y-%m-%d %H:%M:%S') if log.delivered_at else None,
            'error_message': log.error_message
        })
    
    return JsonResponse({'status': 'success', 'logs': log_data}) 


@login_required
def trigger_birthday_notifications(request):
    """Manually trigger birthday notifications for testing"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            test_mode = data.get('test', False)
            
            if test_mode:
                # Send test notification to current user
                success, message = send_push_notification_to_user(
                    request.user,
                    "🧪 Test Birthday Notification",
                    "This is a test birthday notification from NeverForget!",
                    'birthday'
                )
                
                return JsonResponse({
                    'status': 'success' if success else 'error',
                    'message': message
                })
            
            # Check for actual birthdays today
            today = date.today()
            todays_birthdays = []
            
            # Get birthdays for the current user's community
            all_birthdays = BirthdayInfo.objects.filter(community_user_name=request.user)
            
            for birthday in all_birthdays:
                if birthday.birthDate:
                    if birthday.birthDate.month == today.month and birthday.birthDate.day == today.day:
                        todays_birthdays.append(birthday)
            
            if not todays_birthdays:
                return JsonResponse({
                    'status': 'info',
                    'message': 'No birthdays found today in your community.'
                })
            
            # Send notifications for each birthday
            notifications_sent = 0
            for birthday in todays_birthdays:
                title = f"🎉 Birthday Today: {birthday.personName}"
                message = f"It's {birthday.personName}'s birthday today! Don't forget to celebrate! 🎂"
                
                success, msg = send_push_notification_to_user(
                    request.user,
                    title,
                    message,
                    'birthday'
                )
                
                if success:
                    notifications_sent += 1
            
            return JsonResponse({
                'status': 'success',
                'message': f'Successfully sent {notifications_sent} birthday notification(s)',
                'birthdays_found': len(todays_birthdays)
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Only POST requests allowed'}, status=405)