from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('add_birthday', views.addBirthday, name='add_birthday'),
    path('profile', views.profile, name='profile'),
    path('community_member/<int:pk>/', views.community_member, name='community_member'),
    path('editAdminProfile', views.editAdminProfile, name = 'editAdminProfile'),
    path('profile/<str:pk>/', views.formLink , name = 'profile'),
    
    # PWA URLs
    path('api/push-subscription/', views.push_subscription, name='push_subscription'),
    path('api/vapid-public-key/', views.get_vapid_public_key_view, name='vapid_public_key'),
    path('api/vapid-public-key/', views.get_vapid_public_key_view, name='get_vapid_public_key'),
    path('api/send-birthday-notification/', views.send_birthday_notification, name='send_birthday_notification'),
    path('api/notification-preferences/', views.notification_preferences, name='notification_preferences'),
    path('api/notification-logs/', views.notification_logs, name='notification_logs'),
    path('api/trigger-birthday-notifications/', views.trigger_birthday_notifications, name='trigger_birthday_notifications'),
    path('offline/', views.offline_page, name='offline_page'),
    path('sw.js', views.service_worker, name='service_worker'),
    path('manifest.json', views.manifest, name='manifest'),
]