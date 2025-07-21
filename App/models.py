from django.db import models
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
    phoneNumber = models.IntegerField()
    email = models.EmailField(max_length=254)
    matric =  models.CharField(max_length=50)
    department =  models.CharField(max_length=50)
    level = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    trainingLevel = models.CharField(max_length=50, choices=TRAINING_LEVEL_CHOICES, null=True)
    reminderDays = models.IntegerField(null=True)
    
    def __str__(self):
        return self.personName