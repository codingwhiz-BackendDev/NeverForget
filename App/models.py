from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class BirthdayInfo(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    TRAINING_LEVEL_CHOICES = (
        ('baptisimal', 'Baptisimal'),
        ('believers', 'Believers'),
        ('workers-in-training', 'Workers In Training'),
        ('completed', 'Completed'),
    )

    community_user_name = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    personName = models.CharField(max_length=50)
    personImage = models.ImageField(upload_to='Birthday Images', null=True, blank=True)
    birthDate = models.DateField(auto_now=False, auto_now_add=False) 
    phoneNumber = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    matric =  models.CharField(max_length=50)
    department =  models.CharField(max_length=50)
    level = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    trainingLevel = models.CharField(max_length=50, choices=TRAINING_LEVEL_CHOICES, null=True)
    reminderDays = models.IntegerField(null=True)
    
    def __str__(self):
        return self.personName


class AdminProfile(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    community_name = models.CharField(max_length=50, null=True)
    adminImage = models.ImageField(upload_to='Admin Images', null=True, blank=True)
    email = models.EmailField(max_length=254)
    phone_number = PhoneNumberField(region='NG')
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True) 
    
    def __str__(self):
        return str(self.community_name)


class PushSubscription(models.Model):
    """
    Model to store push notification subscriptions for PWA
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_subscriptions')
    endpoint = models.URLField(max_length=500, help_text="Browser's push service URL")
    p256dh_key = models.CharField(max_length=255, help_text="P-256 DH key for encryption")
    auth_key = models.CharField(max_length=255, help_text="Authentication key")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Whether this subscription is active")
    
    class Meta:
        unique_together = ['user', 'endpoint']
        verbose_name = "Push Subscription"
        verbose_name_plural = "Push Subscriptions"
    
    def __str__(self):
        return f"Push Subscription for {self.user.username}"


class NotificationPreference(models.Model):
    """
    Model to store user notification preferences
    """
    REMINDER_CHOICES = (
        (1, '1 day before'),
        (3, '3 days before'),
        (7, '1 week before'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preference')
    birthday_notifications = models.BooleanField(default=True, help_text="Enable birthday notifications")
    reminder_days = models.IntegerField(choices=REMINDER_CHOICES, default=1, help_text="Days before birthday to send reminder")
    notification_time = models.TimeField(default='09:00', help_text="Time to send notifications")
    email_notifications = models.BooleanField(default=True, help_text="Enable email notifications")
    push_notifications = models.BooleanField(default=True, help_text="Enable push notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notification Preference"
        verbose_name_plural = "Notification Preferences"
    
    def __str__(self):
        return f"Notification Preferences for {self.user.username}"


class NotificationLog(models.Model):
    """
    Model to log sent notifications for tracking and debugging
    """
    NOTIFICATION_TYPES = (
        ('birthday', 'Birthday Notification'),
        ('reminder', 'Birthday Reminder'),
        ('welcome', 'Welcome Notification'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_logs')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Notification Log"
        verbose_name_plural = "Notification Logs"
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.notification_type} for {self.user.username} - {self.status}"
