from django.db import models
from products.models import Product
from clients.models import Client
from suppliers.models import Supplier

from django.contrib.auth.models import User
# Create your models here.
Values = [
    ('en attente', 'en attente'),
    ('livré', 'livré'),
]

class ClientOrder(models.Model):
    
    Product       = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="clientorderlist", null=True) # <--- added
    Client        = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="clientorderlist", null=True) # <--- added 
    Quantity      = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True)
    Date          = models.DateField(null=True)
    Status        = models.CharField(max_length=20, choices=Values , blank=False, null=True)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clientorderlist", null=True) # <--- added
    Total         = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True)

  

class SupplierOrder(models.Model):
    
    Product       = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="supplierorderlist", null=True) # <--- added
    Supplier      = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="supplierorderlist", null=True) # <--- added 
    Quantity      = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True)
    Date          = models.DateField( null=True)
    Status        = models.CharField(max_length=20, choices=Values, null=True)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="supplierorderlist", null=True) # <--- added
    Total         = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True)
    
  
