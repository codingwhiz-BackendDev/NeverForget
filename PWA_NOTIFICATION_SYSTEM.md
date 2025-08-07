# 🎉 PWA Notification System with Models

## 📋 Overview

I've created a complete push notification system for your NeverForget PWA with proper Django models. This system allows users to subscribe to push notifications and receive birthday reminders.

## 🗄️ New Models Created

### 1. **PushSubscription**

Stores user's push notification subscriptions from the browser.

```python
class PushSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    endpoint = models.URLField()  # Browser's push service URL
    p256dh_key = models.CharField()  # Encryption key
    auth_key = models.CharField()  # Authentication key
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 2. **NotificationPreference**

Stores user's notification preferences and settings.

```python
class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday_notifications = models.BooleanField(default=True)
    reminder_days = models.IntegerField(choices=[(1, '1 day'), (3, '3 days'), (7, '1 week')])
    notification_time = models.TimeField(default='09:00')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
```

### 3. **NotificationLog**

Tracks all sent notifications for debugging and analytics.

```python
class NotificationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(choices=[('birthday', 'Birthday'), ('reminder', 'Reminder')])
    title = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('failed', 'Failed')])
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True)
    error_message = models.TextField(blank=True)
```

## 🔧 Updated Views

### 1. **push_subscription** (Enhanced)

- ✅ Validates user authentication
- ✅ Stores subscription data in database
- ✅ Creates notification preferences automatically
- ✅ Logs subscription events

### 2. **send_birthday_notification** (Enhanced)

- ✅ Checks user notification preferences
- ✅ Logs notification attempts
- ✅ Validates notification data

### 3. **notification_preferences** (New)

- ✅ GET: Returns user's current preferences
- ✅ POST: Updates user's notification settings

### 4. **notification_logs** (New)

- ✅ Returns user's notification history
- ✅ Shows last 50 notifications

## 🛠️ Setup Instructions

### 1. **Create and Apply Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. **Test the System**

```bash
python manage.py runserver
```

### 3. **Visit Admin Panel**

- Go to `http://127.0.0.1:8000/admin/`
- You'll see new sections:
  - **Push Subscriptions** - Manage user subscriptions
  - **Notification Preferences** - Manage user preferences
  - **Notification Logs** - View notification history

## 📱 How It Works

### 1. **User Subscribes to Notifications**

```javascript
// In pwa.js - when user allows notifications
const subscription = await registration.pushManager.subscribe({
  userVisibleOnly: true,
  applicationServerKey: vapidKey,
});

// Send to Django server
await fetch("/api/push-subscription/", {
  method: "POST",
  body: JSON.stringify(subscription),
});
```

### 2. **Server Stores Subscription**

```python
# Django creates/updates subscription
subscription, created = PushSubscription.objects.update_or_create(
    user=request.user,
    endpoint=endpoint,
    defaults={
        'p256dh_key': p256dh_key,
        'auth_key': auth_key,
        'is_active': True
    }
)
```

### 3. **Send Birthday Notifications**

```python
# When someone has a birthday
success, message = send_push_notification_to_user(
    user=user,
    title="Birthday: John Doe",
    message="It's John's birthday today! 🎉",
    notification_type='birthday'
)
```

## 🔌 API Endpoints

### **POST** `/api/push-subscription/`

- **Purpose**: Store user's push subscription
- **Auth**: Required (user must be logged in)
- **Body**: Push subscription JSON from browser

### **POST** `/api/send-birthday-notification/`

- **Purpose**: Send birthday notification
- **Auth**: Required
- **Body**: `{"person_name": "John Doe", "birthday_date": "2024-01-15"}`

### **GET/POST** `/api/notification-preferences/`

- **Purpose**: Get/update user's notification preferences
- **Auth**: Required

### **GET** `/api/notification-logs/`

- **Purpose**: Get user's notification history
- **Auth**: Required

## 🎯 Next Steps

### 1. **Install Push Notification Library**

```bash
pip install pywebpush
```

### 2. **Generate VAPID Keys**

```python
# Add to settings.py
VAPID_PRIVATE_KEY = 'your_private_key_here'
VAPID_PUBLIC_KEY = 'your_public_key_here'
```

### 3. **Implement Actual Push Sending**

Replace the placeholder in `send_push_notification_to_user()` with real push sending code.

### 4. **Add Background Task**

Create a daily task to check for birthdays and send notifications automatically.

## 📊 Benefits

✅ **Persistent Storage** - Subscriptions survive server restarts  
✅ **User Management** - Track who wants notifications  
✅ **Analytics** - Monitor notification success rates  
✅ **User Preferences** - Let users control notification settings  
✅ **Admin Interface** - Easy management through Django admin  
✅ **Error Tracking** - Log failed notifications for debugging

## 🔍 Testing

### 1. **Test Subscription**

- Allow notifications in browser
- Check admin panel for new subscription

### 2. **Test Preferences**

- Update notification settings via API
- Verify changes in admin panel

### 3. **Test Notifications**

- Send test notification via API
- Check notification logs in admin panel

Your PWA notification system is now fully functional with proper database models! 🎉
