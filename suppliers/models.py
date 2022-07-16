from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User
TYPE_CHOICES  = (('Particulier', 'Particulier'),
               ('Entreprise', 'Entreprise'),
               )


class Supplier(models.Model):
    Type          = models.CharField(max_length=30, choices=TYPE_CHOICES, blank=False)    
    Name          = models.CharField(max_length=100) 
    Phone         = PhoneField(blank=True, help_text='Contact phone number')  
    Reference     = models.CharField(max_length=100)
    Category      = models.CharField(max_length=100)
    Adress        = models.CharField(max_length=100)
    Note          = models.TextField(blank=True, null=True)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="supplierlist", null=True)

    def __str__(self):
        return self.Name
    

    