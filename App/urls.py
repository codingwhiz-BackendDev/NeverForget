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
]
