from django.contrib import admin
from .models import BirthdayInfo, AdminProfile, PushSubscription, NotificationPreference, NotificationLog

# Register your models here.
admin.site.register(BirthdayInfo)
admin.site.register(AdminProfile)


@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'endpoint', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'birthday_notifications', 'reminder_days', 'notification_time', 'push_notifications']
    list_filter = ['birthday_notifications', 'push_notifications', 'email_notifications', 'reminder_days']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'status', 'sent_at']
    list_filter = ['notification_type', 'status', 'sent_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['sent_at', 'delivered_at']
    ordering = ['-sent_at']
    
    def has_add_permission(self, request):
        return False  # Logs should only be created by the system
