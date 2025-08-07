from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from App.models import BirthdayInfo, PushSubscription, NotificationPreference, NotificationLog
from datetime import date
import json
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Check for birthdays today and send push notifications'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Run without sending notifications')
        parser.add_argument('--test', action='store_true', help='Send test notification')

    def handle(self, *args, **options):
        today = date.today()
        dry_run = options['dry_run']
        test_mode = options['test']
        
        if test_mode:
            self.send_test_notifications(dry_run)
            return
        
        self.stdout.write(f"Checking for birthdays on {today.strftime('%Y-%m-%d')}...")
        
        # Find today's birthdays
        todays_birthdays = []
        all_birthdays = BirthdayInfo.objects.all()
        
        for birthday in all_birthdays:
            if birthday.birthDate:
                if birthday.birthDate.month == today.month and birthday.birthDate.day == today.day:
                    todays_birthdays.append(birthday)
        
        if not todays_birthdays:
            self.stdout.write(self.style.WARNING("No birthdays found today."))
            return
        
        self.stdout.write(f"Found {len(todays_birthdays)} birthdays today!")
        
        # Group by community owner
        birthdays_by_community = {}
        for birthday in todays_birthdays:
            if birthday.community_user_name:
                user_id = birthday.community_user_name.id
                if user_id not in birthdays_by_community:
                    birthdays_by_community[user_id] = []
                birthdays_by_community[user_id].append(birthday)
        
        # Send notifications
        notifications_sent = 0
        for user_id, birthdays in birthdays_by_community.items():
            try:
                user = User.objects.get(id=user_id)
                success = self.send_birthday_notification_to_user(user, birthdays, dry_run)
                if success:
                    notifications_sent += 1
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User with ID {user_id} not found"))
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"DRY RUN: Would have sent {notifications_sent} notifications"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Successfully sent {notifications_sent} notifications"))
    
    def send_birthday_notification_to_user(self, user, birthdays, dry_run=False):
        """Send birthday notification to a specific user"""
        try:
            # Check preferences
            try:
                preferences = NotificationPreference.objects.get(user=user)
                if not preferences.birthday_notifications or not preferences.push_notifications:
                    return False
            except NotificationPreference.DoesNotExist:
                preferences = NotificationPreference.objects.create(user=user)
            
            # Check subscriptions
            subscriptions = PushSubscription.objects.filter(user=user, is_active=True)
            if not subscriptions.exists():
                return False
            
            # Create message
            if len(birthdays) == 1:
                birthday = birthdays[0]
                title = f"🎉 Birthday Today: {birthday.personName}"
                message = f"It's {birthday.personName}'s birthday today! Don't forget to celebrate! 🎂"
            else:
                names = [b.personName for b in birthdays]
                title = f"🎉 {len(birthdays)} Birthdays Today!"
                message = f"Today is the birthday of: {', '.join(names)} 🎂"
            
            if dry_run:
                self.stdout.write(f"DRY RUN: Would send to {user.username}: {title}")
                return True
            
            # Log notification
            notification_log = NotificationLog.objects.create(
                user=user,
                notification_type='birthday',
                title=title,
                message=message,
                status='pending'
            )
            
            # Send push notification
            success = self.send_push_notification(user, title, message, notification_log)
            
            if success:
                self.stdout.write(f"✅ Notification sent to {user.username}")
                return True
            else:
                self.stdout.write(f"❌ Failed to send notification to {user.username}")
                return False
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error sending notification to {user.username}: {str(e)}"))
            return False
    
    def send_push_notification(self, user, title, message, notification_log):
        """Send actual push notification using pywebpush"""
        try:
            from pywebpush import webpush, WebPushException
            from django.conf import settings
            
            # Get VAPID keys
            vapid_private_key = getattr(settings, 'VAPID_PRIVATE_KEY', None)
            vapid_claims = getattr(settings, 'VAPID_CLAIMS', {
                'sub': 'mailto:admin@neverforget.com'
            })
            
            if not vapid_private_key:
                self.stdout.write(self.style.WARNING("VAPID_PRIVATE_KEY not configured"))
                notification_log.status = 'failed'
                notification_log.error_message = 'VAPID_PRIVATE_KEY not configured'
                notification_log.save()
                return False
            
            # Get subscriptions
            subscriptions = PushSubscription.objects.filter(user=user, is_active=True)
            
            success_count = 0
            for subscription in subscriptions:
                try:
                    subscription_info = {
                        'endpoint': subscription.endpoint,
                        'keys': {
                            'p256dh': subscription.p256dh_key,
                            'auth': subscription.auth_key
                        }
                    }
                    
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
                        vapid_private_key=vapid_private_key,
                        vapid_claims=vapid_claims
                    )
                    
                    if response.status_code == 200:
                        success_count += 1
                        
                except WebPushException as e:
                    if '410' in str(e) or '404' in str(e):
                        subscription.is_active = False
                        subscription.save()
                except Exception as e:
                    self.stdout.write(f"Error sending to subscription {subscription.id}: {str(e)}")
            
            # Update log
            if success_count > 0:
                notification_log.status = 'sent'
                notification_log.delivered_at = timezone.now()
                notification_log.save()
                return True
            else:
                notification_log.status = 'failed'
                notification_log.error_message = 'No successful deliveries'
                notification_log.save()
                return False
                
        except ImportError:
            self.stdout.write(self.style.ERROR("pywebpush library not installed"))
            notification_log.status = 'failed'
            notification_log.error_message = 'pywebpush library not installed'
            notification_log.save()
            return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in send_push_notification: {str(e)}"))
            notification_log.status = 'failed'
            notification_log.error_message = str(e)
            notification_log.save()
            return False
    
    def send_test_notifications(self, dry_run=False):
        """Send test notifications"""
        self.stdout.write("Sending test notifications...")
        
        users_with_subscriptions = User.objects.filter(
            push_subscriptions__is_active=True
        ).distinct()
        
        if not users_with_subscriptions.exists():
            self.stdout.write(self.style.WARNING("No users with active push subscriptions found"))
            return
        
        for user in users_with_subscriptions:
            title = "🧪 Test Notification"
            message = "This is a test push notification from NeverForget!"
            
            if dry_run:
                self.stdout.write(f"DRY RUN: Would send test to {user.username}")
            else:
                success = self.send_birthday_notification_to_user(user, [], dry_run=False)
                if success:
                    self.stdout.write(f"✅ Test notification sent to {user.username}")
                else:
                    self.stdout.write(f"❌ Failed to send test to {user.username}")
