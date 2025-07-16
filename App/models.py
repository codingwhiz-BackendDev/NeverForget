from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class BirthdayInfo(models.Model):
    community_user_name = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    personName = models.CharField(max_length=50)
    personImage = models.ImageField(upload_to='Birthday Images', null=True)
    birthDate = models.DateField(auto_now=False, auto_now_add=False) 
    phoneNumber = models.IntegerField()
    email = models.EmailField(max_length=254)
    matric =  models.CharField(max_length=50)
    department =  models.CharField(max_length=50)
    level = models.IntegerField()
    
    def __str__(self):
        return self.personName